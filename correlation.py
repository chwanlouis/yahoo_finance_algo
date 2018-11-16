import os
import datetime
import pandas as pd
from common import YahooDataDownloader


class TimeSeriesDataCorrelation(object):
    def __init__(self, symbol_list: list, method: str, start_time: datetime.datetime, end_time: datetime.datetime):
        self.symbol_list = symbol_list
        if method == 'pearson' or method == 'kendall' or method == 'spearman':
            print('Correlation calculation method selected : %s' % method)
            self.method = method
        else:
            print('Undefined calculation method selected : %s' % method)
            self.method = 'pearson'
            print('Default calculation method will be used : %s' % self.method)
        self.start_time = start_time
        self.end_time = end_time

    def data_downloader(self, replace=False):
        pending_symbol_list = list()
        for symbol in self.symbol_list:
            file_name = YahooDataDownloader.file_path_generator(symbol)
            if not os.path.isfile(file_name):
                pending_symbol_list.append(symbol)
        downloader = YahooDataDownloader(
            stock_list=pending_symbol_list,
            start_date=self.start_time,
            end_date=self.end_time
        )
        downloader.main()

    def data_preprocess(self):
        fname_list = [YahooDataDownloader.file_path_generator(sym) for sym in self.symbol_list]
        df_list = [pd.read_csv(f_name) for f_name in fname_list]
        df_list = [df.set_index('Date') for df in df_list]
        df_list = [df[['Close']] for df in df_list]
        df = pd.concat(df_list, axis=1, join='outer')
        df.columns = self.symbol_list
        return df.dropna()

    def main(self):
        self.data_downloader()
        df = self.data_preprocess()
        return df.corr(method=self.method)


if __name__ == '__main__':
    symbol_list = ['GC=F', '^HSI', 'CL=F','CC=F']
    method = 'pearson'
    start_time = datetime.datetime(year=2017, month=1, day=1)
    end_time = datetime.datetime.today()
    ts_correlation = TimeSeriesDataCorrelation(
        symbol_list=symbol_list,
        method=method,
        start_time=start_time,
        end_time=end_time
    )
    corr_df = ts_correlation.main()
    print(corr_df)
