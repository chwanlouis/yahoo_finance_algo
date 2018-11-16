import os
import datetime
import fix_yahoo_finance as yf


def getting_symbol_name(stock: str):
    hsi_constituent_dict = {
        "0001.HK": "CKH HOLDINGS",
        "0002.HK": "CLP HOLDINGS",
        "0003.HK": "HK & CHINA GAS",
        "0005.HK": "HSBC HOLDINGS",
        "0006.HK": "POWER ASSETS",
        "0011.HK": "HANG SENG BANK",
        "0012.HK": "HENDERSON LAND",
        "0016.HK": "SHK PPT",
        "0017.HK": "NEW WORLD DEV",
        "0019.HK": "SWIRE PACIFIC A",
        "0027.HK": "GALAXY ENT",
        "0066.HK": "MTR CORPORATION",
        "0083.HK": "SINO LAND",
        "0101.HK": "HANG LUNG PPT",
        "0151.HK": "WANT WANT CHINA",
        "0175.HK": "GEELY AUTO",
        "0267.HK": "CITIC",
        "0288.HK": "WH GROUP",
        "0386.HK": "SINOPEC CORP",
        "0388.HK": "HKEX",
        "0688.HK": "CHINA OVERSEAS",
        "0700.HK": "TENCENT",
        "0762.HK": "CHINA UNICOM",
        "0823.HK": "LINK REIT",
        "0836.HK": "CHINA RES POWER",
        "0857.HK": "PETROCHINA",
        "0883.HK": "CNOOC",
        "0939.HK": "CCB",
        "0941.HK": "CHINA MOBILE",
        "1038.HK": "CKI HOLDINGS",
        "1044.HK": "HENGAN INT'L",
        "1088.HK": "CHINA SHENHUA",
        "1093.HK": "CSPC PHARMA",
        "1109.HK": "CHINA RES LAND",
        "1113.HK": "CK ASSET",
        "1177.HK": "SINO BIOPHARM",
        "1299.HK": "AIA",
        "1398.HK": "ICBC",
        "1928.HK": "SANDS CHINA LTD",
        "1997.HK": "WHARF REIC",
        "2007.HK": "COUNTRY GARDEN",
        "2018.HK": "AAC TECH",
        "2313.HK": "SHENZHOU INTL",
        "2318.HK": "PING AN",
        "2319.HK": "MENGNIU DAIRY",
        "2382.HK": "SUNNY OPTICAL",
        "2388.HK": "BOC HONG KONG",
        "2628.HK": "CHINA LIFE",
        "3328.HK": "BANKCOMM",
        "3988.HK": "BANK OF CHINA"
    }
    if stock in hsi_constituent_dict.keys():
        return hsi_constituent_dict[stock]
    return None


def get_stock_sub_indexes(stock: str):
    sub_index_category = {
        "Finance": ["0005.HK", "0011.HK", "0388.HK", "0939.HK", "1299.HK", "1398.HK", "2318.HK", "2388.HK", "2628.HK",
                    "3328.HK", "3988.HK"],
        "Utilities": ["0002.HK", "0003.HK", "0006.HK", "0836.HK", "1038.HK"],
        "Properties": ["0012.HK", "0016.HK", "0017.HK", "0083.HK", "0101.HK", "0688.HK", "0823.HK", "1109.HK", "1113.HK",
                       "1997.HK", "2007.HK"],
        "Commerce & Industry": ["0001.HK", "0019.HK", "0027.HK", "0066.HK", "0151.HK", "0175.HK", "0267.HK", "0288.HK",
                                "0386.HK", "0700.HK", "0762.HK", "0857.HK", "0883.HK", "0941.HK", "1044.HK", "1088.HK",
                                "1093.HK", "1177.HK", "1928.HK", "2018.HK", "2313.HK", "2319.HK", "2382.HK"]
    }
    for category, stock_list in sub_index_category.items():
        if stock in stock_list:
            return category
    return None


class YahooDataDownloader(object):
    def __init__(self, stock_list: list, start_date: datetime.datetime, end_date: datetime.datetime):
        self.stock_list = stock_list
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def file_path_generator(symbol: str):
        symbol = symbol.replace('.', '').replace('^', 'index_')
        return 'dataset/%s.csv' % symbol

    def downloader(self, symbol: str):
        file_path = self.file_path_generator(symbol)
        data = yf.download(symbol, start=self.start_date, end=self.end_date)
        data.to_csv(file_path)
        print("File generated : %s" % file_path)

    def main(self):
        if not os.path.isdir('dataset'):
            os.mkdir('dataset')
        for symbol in self.stock_list:
            self.downloader(symbol)


if __name__ == '__main__':
    hsi_symbol_list = [
        "0001.HK", "0002.HK", "0003.HK", "0005.HK", "0006.HK", "0011.HK", "0012.HK", "0016.HK", "0017.HK", "0019.HK",
        "0027.HK", "0066.HK", "0083.HK", "0101.HK", "0151.HK", "0175.HK", "0267.HK", "0288.HK", "0386.HK", "0388.HK",
        "0688.HK", "0700.HK", "0762.HK", "0823.HK", "0836.HK", "0857.HK", "0883.HK", "0939.HK", "0941.HK", "1038.HK",
        "1044.HK", "1088.HK", "1093.HK", "1109.HK", "1113.HK", "1177.HK", "1299.HK", "1398.HK", "1928.HK", "1997.HK",
        "2007.HK", "2018.HK", "2313.HK", "2318.HK", "2319.HK", "2382.HK", "2388.HK", "2628.HK", "3328.HK", "3988.HK",
        "^HSNF", "^HSNP", "^HSNU", "^HSNC", "^HSI"
    ]
    commodity_symbol_list = [
        "GC=F", "SI=F", "HG=F", "CL=F", "BZ=F", "NG=F", "C=F", "O=F", "KW=F", "RR=F", "S=F", "FC=F", "LH=F", "LC=F",
        "CC=F", "KC=F", "CT=F", "LB=F", "OJ=F", "SB=F"
    ]
    fx_symbol_list = [
        "HKDCNY=X", "EURHKD=X", "GBPHKD=X", "JPYHKD=X", "AUDHKD=X", "NZDHKD=X", "CADHKD=X", "HKDTWD=X", "HKDTHB=X",
        "KRWHKD=X", "SGDHKD=X", "CHFHKD=X", "VNDHKD=X", "IDRHKD=X", "MOPHKD=X", "EURUSD=X", "GBPUSD=X", "JPY=X",
        "CHF=X", "AUDUSD=X", "NZDUSD=X", "EURGBP=X", "EURCHF=X", "CNY=X", "CAD=X"
    ]
    yahoo_data_handler = YahooDataDownloader(
        stock_list=hsi_symbol_list+commodity_symbol_list+fx_symbol_list,
        start_date=datetime.datetime(2017, 1, 1),
        end_date=datetime.datetime.today()
    )
    yahoo_data_handler.main()
