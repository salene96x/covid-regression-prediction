import json
class QualityChecker:
    def __init__(self, df) -> None:
        self.df = df
        self.body = {
            "Info" : self.get_info(),
            "Duplicated" : int(self.check_duplicated()),
            "Null" : self.check_real_entry_na()['0']
        }
    def get_info(self) -> dict:
        return self.df.info()
    def check_duplicated(self) -> int:
        return self.df.duplicated().sum()
    def check_na(self) -> int:
        result = self.df.isna().sum()
        df = result.to_frame()
        return json.loads(df.to_json())
    def get_check_result(self):
        return self.body
    def check_real_entry_na(self):
        na_result = self.check_na()
        cols = list(self.df.columns)
        for x in cols:
            result = self.df.loc[(self.df[x] == "") | (self.df[x] == 0)]
            na_result["0"][x] += result.shape[0]
        return na_result
            