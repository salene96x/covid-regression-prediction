import pandas as pd
class Cleaner:
    def __init__(self, pandas_data: pd.DataFrame) -> None:
        self.df = pandas_data

    def drop_rows(self, expression : str, reset_index : bool):
        self.df = self.df.drop(self.df.loc[eval(expression.replace('df', 'self.df'))].index)
        if reset_index:
            return self.df.reset_index()
        else :
            return self.df
    
    def drop_columns(self, columns, conditions=None, inplace=False, axis=0):
        '''
        conditions => [df["country"] == "Thailand"]
        columns => ['country', 'iso']
        '''
        self.df = self.df.drop(columns=columns, inplace=True, axis=2)
        return self.df
    def drop_duplicated(self, conditions=None, inplace=False, axis=0):
        '''
        conditions => [df["country"] == "Thailand"]
        '''
        self.df = self.df.drop_duplicated(inplace=inplace, axis=axis) 
        return self.df
