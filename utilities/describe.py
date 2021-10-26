import pandas as pd
import numpy as np
import os.path, math, sys

class Describe:
    def __init__(self, path : str) -> None:
        self.df     : pd.DataFrame()
        self.stat   : pd.DataFrame()

        self.open_dataset(path)
        self.fill_stat()

    def open_dataset(self, path : str):
        if not os.path.isfile(path) :
            print("\nWrong path for dataset\n")
            exit(1)

        self.df = pd.read_csv(path)
        if self.df.columns[0] == 'Index':
            self.df = self.df.set_index('Index')

    def fill_stat(self):
        self.stat = pd.DataFrame(index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])

        for col in self.df.columns:
            if self.df[col].dtype == float:             # Get stat only for float types
                collector   = []
                np_col      = self.df[col].values       # Create a numpy array from pandas column
                np_col      = np_col[~np.isnan(np_col)] # Delete all NaN beafore calculation
                np_col.sort()                           # Sort everything make life easier

                collector.append(float(len(np_col)))                    # COUNT
                collector.append(sum(np_col) / collector[0])            # MEAN
                collector.append(self.get_std_dev(collector, np_col))   # STD
                collector.append(np_col[0])                             # MIN
                collector.append(self.get_percentile(0.25, np_col))     # 25%
                collector.append(self.get_percentile(0.50, np_col))     # 50%
                collector.append(self.get_percentile(0.75, np_col))     # 75%
                collector.append(np_col[-1])                            # MAX

                self.stat[col] = collector  # Add column stats to the DataFrame

    def get_std_dev(self, collector , np_col : np.array([])) -> float:
        lenCol  = collector[0]
        mean    = collector[1]
        var     = sum((x - mean)**2 for x in np_col) / lenCol
        std_dev = var ** 0.5
        
        return ( std_dev )

    def get_percentile(self, percent, np_col : np.array([])) -> float:
        k = (len(np_col) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)

        if f == c:
            ret = np_col[int(k)]
        else:
            d0  = np_col[int(f)] * (c - k)
            d1  = np_col[int(c)] * (k - f)
            ret = d0 + d1
        
        return ( ret )



##################################################################################

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nUsage : Describe.py PathToDatasetFile\n')
        exit(1)

    describe = Describe(sys.argv[1])
    print(describe.stat)
