import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==========================================
# CLASS 1: KONFIGURASI PENGATURAN
# ==========================================
class Config:
    TICKERS1 = ["BBCA", "BBRI", "BMRI", "BREN"] # Nama saham bersih
    TICKERS = [
            "AALI", "ABBA", "ABDA", "ABMM", "ACES", "ACST", "ADES", "ADHI", "ADMF", "ADMG", "ADRO", "AGII", "AGRO", "AGRS",
            "AHAP", "AIMS", "AISA", "AKKU", "AKPI", "AKRA", "AKSI", "ALDO", "ALKA", "ALMI", "ALTO", "AMAG", "AMFG", "AMIN",
            "AMRT", "ANJT", "ANTM", "APEX", "APIC", "APII", "APLI", "APLN", "ARGO", "ARII", "ARNA", "ARTA", "ARTI", "ARTO",
            "ASBI", "ASDM", "ASGR", "ASII", "ASJT", "ASMI", "ASRI", "ASRM", "ASSA", "ATIC", "AUTO", "BABP", "BACA", "BAJA",
            "BALI", "BAPA", "BATA", "BAYU", "BBCA", "BBHI", "BBKP", "BBLD", "BBMD", "BBNI", "BBRI", "BBRM", "BBTN", "BBYB",
            "BCAP", "BCIC", "BCIP", "BDMN", "BEKS", "BEST", "BFIN", "BGTG", "BHIT", "BIKA", "BIMA", "BINA", "BIPI", "BIPP",
            "BIRD", "BISI", "BJBR", "BJTM", "BKDP", "BKSL", "BKSW", "BLTA", "BLTZ", "BMAS", "BMRI", "BMSR", "BMTR", "BNBA",
            "BNBR", "BNGA", "BNII", "BNLI", "BOLT", "BPFI", "BPII", "BRAM", "BRMS", "BRNA", "BRPT", "BSDE", "BSIM", "BSSR",
            "BSWD", "BTEK", "BTEL", "BTON", "BTPN", "BUDI", "BUKK", "BULL", "BUMI", "BUVA", "BVIC", "BWPT", "BYAN", "CANI",
            "CASS", "CEKA", "CENT", "CFIN", "CINT", "CITA", "CLPI", "CMNP", "CMPP", "CNKO", "CNTX", "COWL", "CPIN", "CPRO",
            "CSAP", "CTBN", "CTRA", "CTTH", "DART", "DEFI", "DEWA", "DGIK", "DILD", "DKFT", "DLTA", "DMAS", "DNAR", "DNET",
            "DOID", "DPNS", "DSFI", "DSNG", "DSSA", "DUTI", "DVLA", "DYAN", "ECII", "EKAD", "ELSA", "ELTY", "EMDE", "EMTK",
            "ENRG", "EPMT", "ERAA", "ERTX", "ESSA", "ESTI", "ETWA", "EXCL", "FAST", "FASW", "FISH", "FMII", "FORU", "FPNI",
            "GAMA", "GDST", "GDYR", "GEMA", "GEMS", "GGRM", "GIAA", "GJTL", "GLOB", "GMTD", "GOLD", "GOLL", "GPRA", "GSMF",
            "GTBO", "GWSA", "GZCO", "HADE", "HDFA", "HDTX", "HERO", "HEXA", "HITS", "HMSP", "HOME", "HOTL", "HRUM", "IATA",
            "IBFN", "IBST", "ICBP", "ICON", "IGAR", "IIKP", "IKAI", "IKBI", "IMAS", "IMJS", "IMPC", "INAF", "INAI", "INCI",
            "INCO", "INDF", "INDR", "INDS", "INDX", "INDY", "INKP", "INPC", "INPP", "INRU", "INTA", "INTD", "INTP", "IPOL",
            "ISAT", "ISSP", "ITMA", "ITMG", "JAWA", "JECC", "JIHD", "JKON", "JKSW", "JPFA", "JRPT", "JSMR", "JSPT", "JTPE",
            "KAEF", "KARW", "KBLI", "KBLM", "KBLV", "KBRI", "KDSI", "KIAS", "KICI", "KIJA", "KKGI", "KLBF", "KOBX", "KOIN",
            "KONI", "KOPI", "KPIG", "KRAH", "KRAS", "KREN", "LAPD", "LCGP", "LEAD", "LINK", "LION", "LMAS", "LMPI", "LMSH",
            "LPCK", "LPGI", "LPIN", "LPKR", "LPLI", "LPPF", "LPPS", "LRNA", "LSIP", "LTLS", "MAGP", "MAIN", "MAMI", "MAPI",
            "MAYA", "MBAP", "MBSS", "MBTO", "MCOR", "MDIA", "MDKA", "MDLN", "MDRN", "MEDC", "MEGA", "MERK", "META",
            "MFMI", "MGNA", "MICE", "MIDI", "MIKA", "MIRA", "MITI", "MKPI", "MLBI", "MLIA", "MLPL", "MLPT", "MMLP",
            "MNCN", "MPMX", "MPPA", "MRAT", "MREI", "MSKY", "MTDL", "MTFN", "MTLA", "MTSM", "MYOH", "MYOR", "MYRX", "MYTX",
            "NELY", "NIKL", "NIPS", "NIRO", "NISP", "NOBU", "NRCA", "OCAP", "OKAS", "OMRE", "PADI", "PALM", "PANR", "PANS",
            "PBRX", "PDES", "PEGE", "PGAS", "PGLI", "PICO", "PJAA", "PKPK", "PLAS", "PLIN", "PNBN", "PNBS", "PNIN", "PNLF",
            "PNSE", "POLY", "POOL", "PPRO", "PRAS", "PSAB", "PSDN", "PSKT", "PTBA", "PTIS", "PTPP", "PTRO", "PTSN", "PTSP",
            "PUDP", "PWON", "PYFA", "RAJA", "RALS", "RANC", "RBMS", "RDTX", "RELI", "RICY", "RIGS", "RIMO", "RODA", "ROTI",
            "RUIS", "SAFE", "SAME", "SCCO", "SCMA", "SCPI", "SDMU", "SDPC", "SDRA", "SGRO", "SHID", "SIDO", "SILO", "SIMA",
            "SIMP", "SIPD", "SKBM", "SKLT", "SKYB", "SMAR", "SMBR", "SMCB", "SMDM", "SMDR", "SMGR", "SMMA", "SMMT", "SMRA",
            "SMRU", "SMSM", "SOCI", "SONA", "SPMA", "SQMI", "SRAJ", "SRIL", "SRSN", "SRTG", "SSIA", "SSMS", "SSTM", "STAR",
            "STTP", "SUGI", "SULI", "SUPR", "TALF", "TARA", "TAXI", "TBIG", "TBLA", "TBMS", "TCID", "TELE", "TFCO", "TGKA",
            "TIFA", "TINS", "TIRA", "TIRT", "TKIM", "TLKM", "TMAS", "TMPO", "TOBA", "TOTL", "TOTO", "TOWR", "TPIA", "TPMA",
            "TRAM", "TRIL", "TRIM", "TRIO", "TRIS", "TRST", "TRUS", "TSPC", "ULTJ", "UNIC", "UNIT", "UNSP", "UNTR", "UNVR",
            "VICO", "VINS", "VIVA", "VOKS", "VRNA", "WAPO", "WEHA", "WICO", "WIIM", "WIKA", "WINS", "WOMF", "WSKT", "WTON",
            "YPAS", "YULE", "ZBRA", "SHIP", "CASA", "DAYA", "DPUM", "IDPR", "JGLE", "KINO", "MARI", "MKNT", "MTRA", "OASA",
            "POWR", "INCF", "WSBP", "PBSA", "PRDA", "BOGA", "BRIS", "PORT", "CARS", "MINA", "FORZ", "CLEO", "TAMU", "CSIS",
            "TGRA", "FIRE", "TOPS", "KMTR", "ARMY", "MAPB", "WOOD", "HRTA", "MABA", "HOKI", "MPOW", "MARK", "NASA", "MDKI",
            "BELL", "KIOS", "GMFI", "MTWI", "ZINC", "MCAS", "PPRE", "WEGE", "PSSI", "MORA", "DWGL", "PBID", "JMAS", "CAMP",
            "IPCM", "PCAR", "LCKM", "BOSS", "HELI", "JSKY", "INPS", "GHON", "TDPM", "DFAM", "NICK", "BTPS", "SPTO", "PRIM",
            "HEAL", "TRUK", "PZZA", "TUGU", "MSIN", "SWAT", "KPAL", "TNCA", "MAPA", "TCPI", "IPCC", "RISE", "BPTR", "POLL",
            "NFCX", "MGRO", "NUSA", "FILM", "ANDI", "LAND", "MOLI", "PANI", "DIGI", "CITY", "SAPX", "KPAS", "SURE", "HKMU",
            "MPRO", "DUCK", "GOOD", "SKRN", "YELO", "CAKK", "SATU", "SOSS", "DEAL", "POLA", "DIVA", "LUCK", "URBN", "SOTS",
            "ZONE", "PEHA", "FOOD", "BEEF", "POLI", "CLAY", "NATO", "JAYA", "COCO", "MTPS", "CPRI", "HRME", "POSA", "JAST",
            "FITT", "BOLA", "CCSI", "SFAN", "POLU", "KJEN", "KAYU", "ITIC", "PAMG", "IPTV", "BLUE", "ENVY", "EAST", "LIFE",
            "FUJI", "KOTA", "INOV", "ARKA", "SMKL", "HDIT", "KEEN", "BAPI", "TFAS", "GGRP", "OPMS", "NZIA", "SLIS", "PURE",
            "IRRA", "DMMX", "SINI", "WOWS", "ESIP", "TEBE", "KEJU", "PSGO", "AGAR", "IFSH", "REAL", "IFII", "PMJS", "UCID",
            "GLVA", "PGJO", "AMAR", "CSRA", "INDO", "AMOR", "TRIN", "DMND", "PURA", "PTPW", "TAMA", "IKAN", "AYLS", "DADA",
            "ASPI", "ESTA", "BESS", "AMAN", "CARE", "SAMF", "SBAT", "KBAG", "CBMF", "RONY", "CSMI", "BBSS", "BHAT", "CASH",
            "TECH", "EPAC", "UANG", "PGUN", "SOFA", "PPGL", "TOYS", "SGER", "TRJA", "PNGO", "SCNP", "BBSI", "KMDS", "PURI",
            "SOHO", "HOMI", "ROCK", "ENZO", "PLAN", "PTDU", "ATAP", "VICI", "PMMP", "WIFI", "FAPA", "DCII", "KETR", "DGNS",
            "UFOE", "BANK", "WMUU", "EDGE", "UNIQ", "BEBS", "SNLK", "ZYRX", "LFLO", "FIMP", "TAPG", "NPGF", "LUCY", "ADCP",
            "HOPE", "MGLV", "TRUE", "LABA", "ARCI", "IPAC", "MASB", "BMHS", "FLMC", "NICL", "UVCR", "BUKA", "HAIS", "OILS",
            "GPSO", "MCOL", "RSGK", "RUNS", "SBMA", "CMNT", "GTSI", "IDEA", "KUAS", "BOBA", "MTEL", "DEPO", "BINO", "CMRY",
            "WGSH", "TAYS", "WMPP", "RMKE", "OBMD", "AVIA", "IPPE", "NASI", "BSML", "DRMA", "ADMR", "SEMA", "ASLC", "NETV",
            "BAUT", "ENAK", "NTBK", "SMKM", "STAA", "NANO", "BIKE", "WIRG", "SICO", "GOTO", "TLDN", "MTMH", "WINR", "IBOS",
            "OLIV", "ASHA", "SWID", "TRGU", "ARKO", "CHEM", "DEWI", "AXIO", "KRYA", "HATM", "RCCC", "GULA", "JARR", "AMMS",
            "RAFI", "KKES", "ELPI", "EURO", "KLIN", "TOOL", "BUAH", "CRAB", "MEDS", "COAL", "PRAY", "CBUT", "BELI", "MKTR",
            "OMED", "BSBK", "PDPP", "KDTN", "ZATA", "NINE", "MMIX", "PADA", "ISAP", "VTNY", "SOUL", "ELIT", "BEER", "CBPE",
            "SUNI", "CBRE", "WINE", "BMBL", "PEVE", "LAJU", "FWCT", "NAYZ", "IRSX", "PACK", "VAST", "CHIP", "HALO", "KING",
            "PGEO", "FUTR", "HILL", "BDKR", "PTMP", "SAGE", "TRON", "CUAN", "NSSS", "GTRA", "HAJJ", "PIPA", "NCKL", "MENN",
            "AWAN", "MBMA", "RAAM", "DOOH", "JATI", "TYRE", "MPXL", "SMIL", "KLAS", "MAXI", "VKTR", "RELF", "AMMN", "CRSN",
            "GRPM", "WIDI", "TGUK", "INET", "MAHA", "RMKO", "CNMA", "FOLK", "HBAT", "GRIA", "PPRI", "ERAL", "CYBR", "MUTU",
            "LMAX", "HUMI", "MSIE", "RSCH", "BABY", "AEGS", "IOTF", "KOCI", "PTPS", "BREN", "STRK", "KOKA", "LOPI", "UDNG",
            "RGAS", "MSTI", "IKPM", "AYAM", "SURI", "ASLI", "CGAS", "NICE", "MSJA", "SMLE", "ACRO", "MANG", "GRPH", "SMGA",
            "UNTD", "TOSK", "MPIX", "ALII", "MKAP", "MEJA", "LIVE", "HYGN", "BAIK", "VISI", "AREA", "MHKI", "ATLA", "DATA",
            "SOLA", "BATR", "SPRE", "PART", "GOLF", "ISEA", "BLES", "GUNA", "LABS", "DOSS", "NEST", "PTMR", "VERN", "DAAZ",
            "BOAT", "NAIK", "AADI", "MDIY", "KSIX", "RATU", "YOII", "HGII", "BRRC", "DGWG", "CBDK", "OBAT", "MINE", "KAQI",
            "YUPI", "FORE", "MDLA", "DKHH", "PSAT", "CDIA", "COIN", "BLOG", "CHEK", "MERI", "ASPR", "PMUI", "EMAS", "PJHB",
            "RLCO", "SUPA"
        ]
  
    PERIOD = "1y"
    TEMPLATE_FILE = "template.html"
    OUTPUT_FILE = "index.html"

# ==========================================
# CLASS 2: RUMUS INDIKATOR (STATIC METHODS)
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

# ==========================================
# CLASS 3: ANALISATOR SAHAM (PROSES 1 SAHAM)
# ==========================================
class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yf_ticker = f"{ticker}.JK" # Format untuk Yahoo Finance
        self.df = pd.DataFrame()

    def fetch_data(self):
        """Menarik data dari Yahoo Finance"""
        df = yf.download(self.yf_ticker, period=Config.PERIOD, progress=False)
        if df.empty:
            return False
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        self.df = df
        return True

    def calculate_signals(self):
        """Menghitung semua indikator dan sinyal Buy/Sell"""
        self.df['HHMA'] = Indicators.calc_hhma(self.df['Close'])
        self.df['EMA9'] = ta.ema(self.df['Close'], length=9)
        self.df['EMA21'] = ta.ema(self.df['Close'], length=21)
        
        # Logika Tren HHMA
        self.df['isBullish'] = self.df['HHMA'] > self.df['HHMA'].shift(1)
        self.df['turned_bullish'] = self.df['isBullish'] & (~self.df['isBullish'].shift(1).fillna(False))
        self.df['turned_bearish'] = (~self.df['isBullish']) & (self.df['isBullish'].shift(1).fillna(False))
        
        # Kondisi Filter
        self.df['cond_buy'] = self.df['turned_bullish'] & (self.df['Close'] > self.df['HHMA'])
        self.df['cond_sell'] = self.df['turned_bearish']

    def generate_chart_html(self):
        """Membuat chart Plotly dan mengubahnya jadi HTML"""
        df = self.df
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2])
        
        # Plot Harga & Indikator
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['HHMA'], line=dict(color='blue', width=2), name="HHMA"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], line=dict(color='yellow', width=1), name="EMA 9"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA21'], line=dict(color='orange', width=1), name="EMA 21"), row=1, col=1)
        
        # Label BUY & SELL
        buy_data = df[df['cond_buy']]
        sell_data = df[df['cond_sell']]
        
        fig.add_trace(go.Scatter(x=buy_data.index, y=buy_data['Low'] * 0.98, mode='markers+text', marker=dict(symbol='triangle-up', size=12, color='green'), text=["BUY"]*len(buy_data), textposition="bottom center", name="BUY"), row=1, col=1)
        fig.add_trace(go.Scatter(x=sell_data.index, y=sell_data['High'] * 1.02, mode='markers+text', marker=dict(symbol='triangle-down', size=12, color='red'), text=["SELL"]*len(sell_data), textposition="top center", name="SELL"), row=1, col=1)

        # Plot Volume
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='gray'), row=2, col=1)
        
        fig.update_layout(title=f"Chart Saham: {self.ticker}", xaxis_rangeslider_visible=False, template="plotly_dark", height=600)
        return fig.to_html(full_html=False, include_plotlyjs='cdn')

# ==========================================
# CLASS 4: MAIN APP (PENGENDALI UTAMA)
# ==========================================
class ScreenerApp:
    def __init__(self):
        self.charts_html = ""

    def run(self):
        """Fungsi utama yang menjalankan seluruh proses"""
        print("Mulai menganalisa saham...")
        for ticker in Config.TICKERS:
            try:
                print(f"-> Memproses {ticker}...")
                analyzer = StockAnalyzer(ticker)
                
                if not analyzer.fetch_data():
                    print(f"   [!] Data {ticker} kosong atau tidak ditemukan.")
                    continue
                    
                analyzer.calculate_signals()
                chart_div = analyzer.generate_chart_html()
                
                # Tambahkan chart ke keranjang
                self.charts_html += f"<div class='chart-box'>{chart_div}</div>\n"
                
            except Exception as e:
                print(f"   [!] Error pada {ticker}: {e}")
                self.charts_html += f"<div class='error-msg'>Gagal memuat {ticker}: {str(e)}</div>\n"

        self.inject_to_html()

    def inject_to_html(self):
        """Membaca template.html, menyuntikkan chart, dan menyimpan index.html"""
        if not os.path.exists(Config.TEMPLATE_FILE):
            print(f"CRITICAL ERROR: File {Config.TEMPLATE_FILE} tidak ditemukan!")
            return

        with open(Config.TEMPLATE_FILE, "r", encoding="utf-8") as file:
            template_content = file.read()

        # Suntikkan keranjang chart ke dalam "lubang" template
        final_html = template_content.replace("", self.charts_html)

        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(final_html)
            
        print(f"SELESAI! File {Config.OUTPUT_FILE} berhasil diperbarui.")

# Eksekusi Program Utama
if __name__ == "__main__":
    app = ScreenerApp()
    app.run()
