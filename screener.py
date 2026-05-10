import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

# ==========================================
# 1. RUMUS INDIKATOR HHMA & EMA
# ==========================================
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

def calc_ema(src_series, length):
    return src_series.ewm(span=length, adjust=False).mean()

# ==========================================
# 2. MESIN SCREENER (PENCARI SINYAL)
# ==========================================
def run_screener(tickers):
    buy_rows_html = ""
    sell_rows_html = ""
    buy_count = 0
    sell_count = 0
    
    for ticker in tickers:
        try:
            yf_ticker = f"{ticker}.JK"
            df = yf.download(yf_ticker, period="6mo", interval="1d", progress=False)
            
            if df.empty or len(df) < 30: 
                continue
            
            # Format Kolom Yahoo Finance Terbaru
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Hitung Indikator
            df['HHMA'] = calc_hhma(df['Close'])
            df['EMA9'] = calc_ema(df['Close'], 9)
            df['EMA21'] = calc_ema(df['Close'], 21)
            df['SMA20_Vol'] = df['Volume'].rolling(20).mean()
            
            df['isBullish'] = df['HHMA'] > df['HHMA'].shift(1)
            df['turned_bullish'] = df['isBullish'] & (~df['isBullish'].shift(1).fillna(False))
            df['turned_bearish'] = (~df['isBullish']) & (df['isBullish'].shift(1).fillna(False))
            
            df['cond_buy'] = df['turned_bullish'] & (df['Close'] > df['HHMA'])
            df['cond_sell'] = df['turned_bearish']
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Jika ada sinyal BUY atau SELL di hari terakhir
            if last['cond_buy'] or last['cond_sell']:
                # Tarik Data Fundamental Cepat
                try:
                    info = yf.Ticker(yf_ticker).info
                    per = info.get('trailingPE', 0)
                    pbv = info.get('priceToBook', 0)
                    per_val = per if isinstance(per, (int, float)) else 0
                    pbv_val = pbv if isinstance(pbv, (int, float)) else 0
                except:
                    per_val, pbv_val = 0, 0
                
                # Format Teks & Angka
                tanggal = df.index[-1].strftime('%Y-%m-%d')
                pola = "<span class='buy'>BUY 🚀</span>" if last['cond_buy'] else "<span class='sell'>SELL ⚠️</span>"
                sort_pola = 1 if last['cond_buy'] else 0
                
                pct_change = ((last['Close'] - prev['Close']) / prev['Close']) * 100
                pct_color = "#00ffaa" if pct_change > 0 else "#ff4444"
                pct_str = f"<span style='color: {pct_color};'>{pct_change:.2f}%</span>"
                
                vol = last['Volume']
                if vol >= 1e9: vol_str = f"{vol/1e9:.2f}B"
                elif vol >= 1e6: vol_str = f"{vol/1e6:.2f}M"
                elif vol >= 1e3: vol_str = f"{vol/1e3:.2f}K"
                else: vol_str = str(vol)
                
                is_spike = vol > (last['SMA20_Vol'] * 1.5)
                
                # LINK WIDGET & ICON TRADINGVIEW
                icon_svg = "<svg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='#888' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'></path><polyline points='15 3 21 3 21 9'></polyline><line x1='10' y1='14' x2='21' y2='3'></line></svg>"
                tv_icon = f"<a href='https://id.tradingview.com/chart/?symbol=IDX:{ticker}' target='_blank' style='margin-left:8px;' title='Buka di Web Asli TradingView'>{icon_svg}</a>"
                ticker_link = f"<a href='#' onclick='openWidget(\"{ticker}\"); return false;' style='color:#00ffaa; font-weight:bold; text-decoration:none;'>{ticker}</a>"
                
                # Masukkan ke Baris Tabel
                row_html = f"""
                <tr>
                    <td>{ticker_link} {tv_icon}</td>
                    <td>{tanggal}</td>
                    <td data-order='{sort_pola}'>{pola}</td>
                    <td data-order='{last['Close']}'>{last['Close']:,.0f}</td>
                    <td data-order='{pct_change}'>{pct_str}</td>
                    <td data-order='{vol}'>{vol_str}</td>
                    <td>{'Ya 🔥' if is_spike else 'Tidak'}</td>
                    <td>{'Hijau 🟢' if last['isBullish'] else 'Merah 🔴'}</td>
                    <td data-order='{per_val}'>{per_val if per_val != 0 else 'N/A'}</td>
                    <td data-order='{pbv_val}'>{pbv_val if pbv_val != 0 else 'N/A'}</td>
                    <td>{'Uptrend 📈' if last['EMA9'] > last['EMA21'] else 'Downtrend 📉'}</td>
                </tr>
                """
                
                # Pisahkan ke tabel Buy atau Sell
                if last['cond_buy']:
                    buy_rows_html += row_html
                    buy_count += 1
                elif last['cond_sell']:
                    sell_rows_html += row_html
                    sell_count += 1
                    
                print(f"🎯 Sinyal ditemukan: {ticker} (BUY: {last['cond_buy']}, SELL: {last['cond_sell']})")
                
        except Exception as e:
            pass # Lanjut jika saham error/delisting
            
    return buy_rows_html, sell_rows_html, buy_count, sell_count

# ==========================================
# 3. EKSEKUSI & PEMBUATAN HTML
# ==========================================
# Masukkan semua daftar saham Anda di sini (tanpa .JK)
daftar_saham1 = [
    "AALI", "ABBA", "ABDA", "ABMM", "ACES", "ACST", "ADES", "ADHI", "ADMF", "ADMG", "ADRO", "AGII", "AGRO", "AGRS",
    "AHAP", "AIMS", "AISA", "AKKU", "AKPI", "AKRA", "AKSI", "ALDO", "ALKA", "ALMI", "ALTO", "AMAG", "AMFG", "AMIN",
    "BBCA", "BBRI", "BMRI", "BBNI", "BREN", "AMMN", "GOTO", "TLKM" 
    # (Catatan: Paste keseluruhan list ratusan saham Anda ke dalam sini)
]
daftar_saham = [
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

print("Mulai menganalisa saham...")
buy_rows, sell_rows, buy_total, sell_total = run_screener(daftar_saham)

waktu_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Header Tabel (Format Kolom)
table_header = """
    <thead>
        <tr>
            <th>Ticker</th>
            <th>Tanggal</th>
            <th>Pola</th>
            <th>Close</th>
            <th>% Ubah</th>
            <th>Volume</th>
            <th>Spike Vol?</th>
            <th>Kernel</th>
            <th>PER</th>
            <th>PBV</th>
            <th>Trend</th>
        </tr>
    </thead>
"""

# --- TEMPLATE HTML DENGAN 2 TABEL (BUY & SELL) ---
html_content = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👑 Stock Screeners - HHMA Strategy</title>
    
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.7.0.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

    <style>
        body {{ background-color: #131722; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; margin: 0; }}
        .container {{ max-width: 1400px; margin: auto; }}
        h1 {{ text-align: center; color: #00ffaa; margin-bottom: 5px; }}
        .subtitle {{ text-align: center; color: #888; margin-bottom: 30px; font-size: 0.9em; }}
        
        .section-title {{ padding-bottom: 10px; margin-top: 40px; border-bottom: 2px solid; }}
        .title-buy {{ color: #00ffaa; border-color: #00ffaa; }}
        .title-sell {{ color: #ff4444; border-color: #ff4444; }}

        table.dataTable {{ width: 100% !important; background-color: #1e222d !important; color: white !important; border-radius: 8px; overflow: hidden; border: none !important; margin-bottom: 40px !important; }}
        table.dataTable thead th {{ background-color: #2a2e39 !important; color: #00ffaa !important; white-space: nowrap; padding: 15px !important; border-bottom: 1px solid #3d4352 !important; }}
        table.dataTable tbody td {{ white-space: nowrap; padding: 12px 15px !important; border-bottom: 1px solid #2a2e39 !important; text-align: center !important; }}
        .dataTables_wrapper .dataTables_filter input, .dataTables_wrapper .dataTables_length select {{ color: white !important; background-color: #2a2e39 !important; border: 1px solid #3d4352 !important; padding: 5px; border-radius: 4px; }}

        /* MODAL WIDGET */
        .modal {{ display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); }}
        .modal-content {{ background-color: #1e222d; margin: 2% auto; padding: 10px; border: 1px solid #00ffaa; border-radius: 8px; width: 90%; height: 85vh; position: relative; }}
        .close {{ position: absolute; right: 15px; top: 5px; color: #ff4444; font-size: 35px; font-weight: bold; cursor: pointer; z-index: 10001; background: #1e222d; padding: 0 10px; border-radius: 50%; }}
        .close:hover {{ color: #fff; background: #ff4444; }}

        .buy {{ color: #00ffaa; font-weight: bold; }}
        .sell {{ color: #ff4444; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👑 HHMA Strategy Screener</h1>
        <div class="subtitle">Terakhir Diperbarui: {waktu_update} UTC | Tahan SHIFT + Klik Header untuk Multiple Sort</div>
        
        <h2 class="section-title title-buy">🟢 Potensi BUY ({buy_total} Saham)</h2>
        <table class="display">
            {table_header}
            <tbody>
                {buy_rows}
            </tbody>
        </table>

        <h2 class="section-title title-sell">🔴 Potensi SELL ({sell_total} Saham)</h2>
        <table class="display">
            {table_header}
            <tbody>
                {sell_rows}
            </tbody>
        </table>
    </div>

    <div id="tv-modal" class="modal">
        <div class="modal-content">
            <span class="close" id="close-modal-btn">&times;</span>
            <div id="tv-widget-container" style="height: 100%; width: 100%;"></div>
        </div>
    </div>

    <script>
        // Inisialisasi DataTables untuk SEMUA tabel yang punya class "display"
        $(document).ready(function() {{
            $('table.display').DataTable({{
                "pageLength": 50,
                "order": [[ 1, "desc" ]],
                "language": {{ "search": "Cari Saham:", "lengthMenu": "Tampilkan _MENU_ data", "emptyTable": "Tidak ada sinyal di kategori ini." }}
            }});
        }});

        function openWidget(ticker) {{
            document.getElementById('tv-modal').style.display = "block";
            new TradingView.widget({{
                "autosize": true, "symbol": "IDX:" + ticker, "interval": "D", "timezone": "Asia/Jakarta",
                "theme": "dark", "style": "1", "locale": "id", "container_id": "tv-widget-container",
                "studies": [ {{ "id": "Aroon@tv-basicstudies", "inputs": {{ "length": 8 }} }}, "Stochastic@tv-basicstudies" ]
            }});
        }}

        const modal = document.getElementById('tv-modal');
        const closeBtn = document.getElementById('close-modal-btn');
        closeBtn.onclick = function() {{ modal.style.display = "none"; document.getElementById('tv-widget-container').innerHTML = ''; }}
        window.onclick = function(event) {{ if (event.target == modal) {{ modal.style.display = "none"; document.getElementById('tv-widget-container').innerHTML = ''; }} }}
    </script>
</body>
</html>
"""

# Tulis langsung ke file index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Berhasil! File index.html digenerate. (BUY: {buy_total}, SELL: {sell_total})")
