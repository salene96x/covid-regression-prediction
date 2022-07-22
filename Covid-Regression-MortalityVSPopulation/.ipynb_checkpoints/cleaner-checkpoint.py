import pandas as pd
class Cleaner:
    def __init__(self, pandas_data: pd.DataFrame) -> None:
        self.df = pandas_data
    def drop_rows(self, conditions: list):
        '''
        conditions =>[(["country"] == "Thailand")]
        '''
        if len(conditions) == 1:
            dropped_rows = self.df.drop(self.df.loc[self.df[conditions[0][0]].index])
            print(dropped_rows)
        else :
            for j in conditions:
                dropped_row = self.df.drop(self.df.loc[self.df[j][0].index])
                print(dropped_rows)
        return self.df
    def drop_columns(self, columns, conditions=None, inplace=False, axis=0):
        '''
        conditions => [df["country"] == "Thailand"]
        columns => ['country', 'iso']
        '''
        self.df.drop(columns=columns, inplace=True, axis=2)
        return self.df