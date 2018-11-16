import pandas as pd


class RelativeRotationalGraphs(object):
    def __init__(self, symbol_list: list, benchmark: str, window_size: int):
        self.symbol_list = symbol_list
        self.benchmark = benchmark
        self.window_size = window_size

    @staticmethod
    def file_path_generator(symbol: str):
        symbol = symbol.replace('.', '').replace('^', 'index_')
        return 'dataset/%s.csv' % symbol

    @staticmethod
    def rs_ratio(prices_df, benchmark, window=10):
        for series in prices_df:
            rs = (prices_df[series].divide(benchmark)) * 100
            rs_ratio = rs.rolling(window).mean()
            rel_ratio = 100 + ((rs_ratio - rs_ratio.mean()) / rs_ratio.std() + 1)
            prices_df[series] = rel_ratio
        prices_df.dropna(axis=0, how='all', inplace=True)
        return prices_df

    @staticmethod
    def rs_momentum(rs_ratio):
        for series in rs_ratio:
            roc = ((rs_ratio[series] / rs_ratio[series].shift(1)) - 1) * 100
            rs_momentum = 100 + ((roc - roc.mean()) / roc.std() + 1)
            rs_ratio[series] = rs_momentum
        rs_ratio.dropna(axis=0, how='all', inplace=True)
        return rs_ratio

    def main(self):
        all_df = list()
        self.symbol_list.append(self.benchmark)
        for symbol in self.symbol_list:
            df = pd.read_csv(self.file_path_generator(symbol))
            df = df.set_index('Date')
            adj_close = df[['Adj Close']]
            adj_close.columns = [symbol]
            all_df.append(adj_close)
        self.symbol_list.pop(-1)
        all_df = pd.concat(all_df, axis=1)
        all_df = all_df.interpolate(method='linear')
        all_df = all_df.dropna()
        symbol_df, benchmark_df = all_df[self.symbol_list], all_df[self.benchmark]
        rs_ratio_df = self.rs_ratio(symbol_df, benchmark_df, 10)
        rs_momentum = self.rs_momentum(rs_ratio_df)


if __name__ == '__main__':
    symbol_list = [
        "0001.HK", "0002.HK", "0003.HK", "0005.HK", "0006.HK", "0011.HK", "0012.HK", "0016.HK", "0017.HK", "0019.HK",
        "0027.HK", "0066.HK", "0083.HK", "0101.HK", "0151.HK", "0175.HK", "0267.HK", "0288.HK", "0386.HK", "0388.HK",
        "0688.HK", "0700.HK", "0762.HK", "0823.HK", "0836.HK", "0857.HK", "0883.HK", "0939.HK", "0941.HK", "1038.HK",
        "1044.HK", "1088.HK", "1093.HK", "1109.HK", "1113.HK", "1177.HK", "1299.HK", "1398.HK", "1928.HK", "1997.HK",
        "2007.HK", "2018.HK", "2313.HK", "2318.HK", "2319.HK", "2382.HK", "2388.HK", "2628.HK", "3328.HK", "3988.HK"
    ]
    rrg_plotter = RelativeRotationalGraphs(
        symbol_list=symbol_list,
        benchmark="^HSI",
        window_size=10
    )
    rrg_plotter.main()
