import yfinance as yf
import pandas as pd
import numpy as np
import os

class Config:
    # TICKERS list bisa Anda tambahkan di sini
    TICKERS1 = ["BBCA", "BBRI", "BMRI", "BREN", "TLDN", "MTMH", "WINR", "IBOS", "OLIV", "ASHA"]
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

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.yf_ticker = f"{ticker}.JK"
        self.df = pd.DataFrame()

    def fetch_data(self):
        df = yf.download(self.yf_ticker, period=Config.PERIOD, progress=False)
        if df.empty: return False
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        self.df = df
        return True

    def calculate_signals(self):
        self.df['HHMA'] = Indicators.calc_hhma(self.df['Close'])
        self.df['EMA9'] = Indicators.calc_ema(self.df['Close'], 9)
        self.df['EMA21'] = Indicators.calc_ema(self.df['Close'], 21)
        self.df['SMA20_Vol'] = self.df['Volume'].rolling(20).mean()
        self.df['isBullish'] = self.df['HHMA'] > self.df['HHMA'].shift(1)
        self.df['turned_bullish'] = self.df['isBullish'] & (~self.df['isBullish'].shift(1).fillna(False))
        self.df['turned_bearish'] = (~self.df['isBullish']) & (self.df['isBullish'].shift(1).fillna(False))
        self.df['cond_buy'] = self.df['turned_bullish'] & (self.df['Close'] > self.df['HHMA'])
        self.df['cond_sell'] = self.df['turned_bearish']

    def has_signal_today(self):
        if self.df.empty: return False
        return bool(self.df.iloc[-1]['cond_buy'] or self.df.iloc[-1]['cond_sell'])

    def get_fundamentals(self):
        try:
            info = yf.Ticker(self.yf_ticker).info
            per = info.get('trailingPE', 0)
            pbv = info.get('priceToBook', 0)
            return per, pbv
        except:
            return 0, 0

    def generate_table_row(self):
        last = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        
        # Format Link
        ticker_link = f"<a href='#' onclick='openWidget(\"{self.ticker}\"); return false;' style='color:#00ffaa; text-decoration:none;'>{self.ticker}</a>"
        icon_svg = "<svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='#888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'></path><polyline points='15 3 21 3 21 9'></polyline><line x1='10' y1='14' x2='21' y2='3'></line></svg>"
        tv_icon = f"<a href='https://id.tradingview.com/chart/?symbol=IDX:{self.ticker}' target='_blank' style='margin-left:5px;'>{icon_svg}</a>"
        
        tanggal = self.df.index[-1].strftime('%Y-%m-%d')
        pola = "<span class='buy-text'>BUY 🚀</span>" if last['cond_buy'] else "<span class='sell-text'>SELL ⚠️</span>"
        
        pct_change = ((last['Close'] - prev['Close']) / prev['Close']) * 100
        pct_color = "#00ffaa" if pct_change > 0 else "#ff4444"
        pct_str = f"<span style='color: {pct_color};'>{pct_change:.2f}%</span>"
        
        vol = last['Volume']
        if vol >= 1e9: vol_str = f"{vol/1e9:.2f}B"
        elif vol >= 1e6: vol_str = f"{vol/1e6:.2f}M"
        elif vol >= 1e3: vol_str = f"{vol/1e3:.2f}K"
        else: vol_str = str(vol)
        
        is_spike = vol > (last['SMA20_Vol'] * 1.5)
        per, pbv = self.get_fundamentals()
        
        # data-order digunakan DataTables untuk sorting angka dibalik teks
        return f"""
        <tr>
            <td>{ticker_link} {tv_icon}</td>
            <td>{tanggal}</td>
            <td>{pola}</td>
            <td data-order='{last['Close']}'>{last['Close']:,.0f}</td>
            <td data-order='{pct_change}'>{pct_str}</td>
            <td data-order='{vol}'>{vol_str}</td>
            <td>{'Ya 🔥' if is_spike else 'Tidak'}</td>
            <td>{'Hijau 🟢' if last['isBullish'] else 'Merah 🔴'}</td>
            <td data-order='{per}'>{per if per != 0 else 'N/A'}</td>
            <td data-order='{pbv}'>{pbv if pbv != 0 else 'N/A'}</td>
            <td>{'Uptrend 📈' if last['EMA9'] > last['EMA21'] else 'Downtrend 📉'}</td>
        </tr>
        """

class ScreenerApp:
    def __init__(self):
        self.rows_html = ""
        self.count = 0

    def run(self):
        for ticker in Config.TICKERS:
            try:
                analyzer = StockAnalyzer(ticker)
                if not analyzer.fetch_data(): continue
                analyzer.calculate_signals()
                if analyzer.has_signal_today():
                    self.rows_html += analyzer.generate_table_row()
                    self.count += 1
            except Exception as e:
                print(f"Error {ticker}: {e}")

        # Gabungkan semua baris ke dalam struktur tabel utuh
        table_full = f"""
        <table id='screenerTable' class='display'>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Tanggal</th>
                    <th>Pola</th>
                    <th>Close</th>
                    <th>% Ubah</th>
                    <th>Volume</th>
                    <th>Spike?</th>
                    <th>Kernel</th>
                    <th>PER</th>
                    <th>PBV</th>
                    <th>Trend</th>
                </tr>
            </thead>
            <tbody>
                {self.rows_html}
            </tbody>
        </table>
        """
        
        if self.count == 0:
            table_full = "<h3 style='text-align:center; color:#888;'>Tidak ada sinyal hari ini.</h3>"
            
        self.inject_to_html(table_full)

    def inject_to_html(self, content):
        with open(Config.TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template = f.read()
        final = template.replace("", content)
        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(final)

if __name__ == "__main__":
    ScreenerApp().run()
