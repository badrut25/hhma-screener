import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==========================================
# CLASS 1: KONFIGURASI PENGATURAN
# ==========================================
class Config:
    # Masukkan ratusan daftar saham Anda di sini
    TICKERS = ["BBCA", "BBRI", "BMRI", "BREN", "TLDN", "MTMH", "WINR", "IBOS", "OLIV", "ASHA"] # Lanjutkan daftar Anda...
    PERIOD = "1y"
    TEMPLATE_FILE = "template.html"
    OUTPUT_FILE = "index.html"

# ==========================================
# CLASS 2: RUMUS INDIKATOR
# ==========================================
class Indicators:
    @staticmethod
    def calc_hhma(src_series, length=24, tension=2.0):
        halfLen = max(1, int(np.floor(length / 2)))
        sqrtLen = max(1, int(np.floor(np.sqrt(length))))
        
        def f_sinh_weight(series, l, t):
            weights = []
            for i in range(l):
                x = (l - i) / l * t
                w = (np.exp(x) - np.exp(-x)) / 2
                weights.append(w)
            weights = np.array(weights)
            weights = weights / np.sum(weights)
            return series.rolling(window=l).apply(lambda vals: np.dot(vals[::-1], weights), raw=True)

        fastSinh = f_sinh_weight(src_series, halfLen, tension)
        slowSinh = f_sinh_weight(src_series, length, tension)
        rawHull = 2 * fastSinh - slowSinh
        return f_sinh_weight(rawHull, sqrtLen, tension)

    @staticmethod
    def calc_ema(src_series, length):
        return src_series.ewm(span=length, adjust=False).mean()

# ==========================================
# CLASS 3: ANALISATOR SAHAM (PROSES 1 SAHAM)
# ==========================================
class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yf_ticker = f"{ticker}.JK"
        self.df = pd.DataFrame()

    def fetch_data(self):
        df = yf.download(self.yf_ticker, period=Config.PERIOD, progress=False)
        if df.empty:
            return False
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        self.df = df
        return True

    def calculate_signals(self):
        self.df['HHMA'] = Indicators.calc_hhma(self.df['Close'])
        self.df['EMA9'] = Indicators.calc_ema(self.df['Close'], 9)
        self.df['EMA21'] = Indicators.calc_ema(self.df['Close'], 21)
        
        self.df['isBullish'] = self.df['HHMA'] > self.df['HHMA'].shift(1)
        self.df['turned_bullish'] = self.df['isBullish'] & (~self.df['isBullish'].shift(1).fillna(False))
        self.df['turned_bearish'] = (~self.df['isBullish']) & (self.df['isBullish'].shift(1).fillna(False))
        
        self.df['cond_buy'] = self.df['turned_bullish'] & (self.df['Close'] > self.df['HHMA'])
        self.df['cond_sell'] = self.df['turned_bearish']

    def has_signal_today(self):
        """Mengecek apakah hari terakhir terdapat sinyal BUY atau SELL"""
        if self.df.empty:
            return False
        last_row = self.df.iloc[-1]
        return bool(last_row['cond_buy'] or last_row['cond_sell'])

    def generate_chart_html(self):
        df = self.df
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2])
        
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['HHMA'], line=dict(color='blue', width=2), name="HHMA"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], line=dict(color='yellow', width=1), name="EMA 9"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA21'], line=dict(color='orange', width=1), name="EMA 21"), row=1, col=1)
        
        buy_data = df[df['cond_buy']]
        sell_data = df[df['cond_sell']]
        
        fig.add_trace(go.Scatter(x=buy_data.index, y=buy_data['Low'] * 0.98, mode='markers+text', marker=dict(symbol='triangle-up', size=12, color='green'), text=["BUY"]*len(buy_data), textposition="bottom center", name="BUY"), row=1, col=1)
        fig.add_trace(go.Scatter(x=sell_data.index, y=sell_data['High'] * 1.02, mode='markers+text', marker=dict(symbol='triangle-down', size=12, color='red'), text=["SELL"]*len(sell_data), textposition="top center", name="SELL"), row=1, col=1)

        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='gray'), row=2, col=1)
        
        # Tambahkan status ke Judul
        status = "🟢 BUY SIGNAL" if df.iloc[-1]['cond_buy'] else "🔴 SELL SIGNAL"
        fig.update_layout(title=f"Chart Saham: {self.ticker} [{status}]", xaxis_rangeslider_visible=False, template="plotly_dark", height=600)
        return fig.to_html(full_html=False, include_plotlyjs='cdn')

# ==========================================
# CLASS 4: MAIN APP (PENGENDALI UTAMA)
# ==========================================
class ScreenerApp:
    def __init__(self):
        self.charts_html = ""
        self.stocks_with_signals = 0 # Menghitung berapa saham yang punya sinyal

    def run(self):
        print("Mulai menganalisa saham...")
        for ticker in Config.TICKERS:
            try:
                analyzer = StockAnalyzer(ticker)
                if not analyzer.fetch_data():
                    print(f"   [-] Data {ticker} tidak ditemukan.")
                    continue
                    
                analyzer.calculate_signals()
                
                # FITUR BARU: Hanya buat chart jika ada sinyal hari ini!
                if analyzer.has_signal_today():
                    print(f"-> 🎯 SINYAL DITEMUKAN pada {ticker}! Sedang menggambar chart...")
                    chart_div = analyzer.generate_chart_html()
                    self.charts_html += f"<div class='chart-box'>{chart_div}</div>\n"
                    self.stocks_with_signals += 1
                else:
                    # Jangan digambar untuk menghemat memori
                    print(f"-> Melewati {ticker} (Tidak ada sinyal)")
                
            except Exception as e:
                print(f"   [!] Error pada {ticker}: {e}")

        # Jika tidak ada satu pun sinyal hari ini
        if self.stocks_with_signals == 0:
            self.charts_html = "<h2 style='text-align:center; color:gray;'>Tidak ada sinyal Buy/Sell hari ini.</h2>"

        self.inject_to_html()

    def inject_to_html(self):
        if not os.path.exists(Config.TEMPLATE_FILE):
            print(f"CRITICAL ERROR: File {Config.TEMPLATE_FILE} tidak ditemukan!")
            return

        with open(Config.TEMPLATE_FILE, "r", encoding="utf-8") as file:
            template_content = file.read()

        # PERBAIKAN BUG REPLACE: Memastikan kata kunci yang diganti itu akurat
        final_html = template_content.replace("", self.charts_html)

        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(final_html)
            
        print(f"SELESAI! Ditemukan {self.stocks_with_signals} saham dengan sinyal hari ini.")

# Eksekusi Program Utama
if __name__ == "__main__":
    app = ScreenerApp()
    app.run()
