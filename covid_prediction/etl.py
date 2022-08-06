import pandas as pd
import numpy as np
class ETL:
    def __init__(self, data_path: str, data_vac_path : str):
        self.data_path = data_path
        self.data_vac_path = data_vac_path
    def get_df(self):
        df = pd.read_csv(self.data_path)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df
    def get_only_tha(self, df):
        df = df.loc[df['location'] == 'Thailand']
        return df
    def mask_values(self, df):
        df['tests_units'] = np.where(df['tests_units'] == 'tests_performed', 1, 0)
        return df
    def drop_columns(self, df):
        columns = [
            'icu_patients_per_million',
            "hosp_patients",
            "hosp_patients_per_million",
            "weekly_icu_admissions",
            'weekly_icu_admissions_per_million',
            "weekly_hosp_admissions",
            'weekly_hosp_admissions_per_million',
            'excess_mortality_cumulative_absolute',             'excess_mortality_cumulative', 'excess_mortality', 'excess_mortality_cumulative_per_million', 'location'
            ]
        df = df.drop(columns=columns)
        df = df.reset_index()
        return df
    def change_specific_values(self, df):
        df.at[515, 'total_vaccinations'] = df.at[514, 'total_vaccinations'] + (df.at[516, 'total_vaccinations'] - df.at[514, 'total_vaccinations'])
        return df
    def mask_total_vaccination_values(self, df):
        df_vac = pd.read_csv('/usr/src/covid_prediction/covid-vaccination-dataset/vaccinations.csv')
        df_vac = df_vac.loc[df_vac['location'] == 'Thailand']
        df_vac['date'] = pd.to_datetime(df_vac['date'], format='%Y-%m-%d')
        df.set_index('date', inplace=True)
        df.update(df_vac.set_index('date'))
        df = df.reset_index()
        return df
    def update_latest(self, df):
        df.at[943, 'total_vaccinations'] = 141814894
        return df
    def fill_na(self, df):
        df = df.fillna(0)
        return df
    def extract_date(self, df):
        df['year'] = df['date'].dt.year
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df = df.drop(columns=["date"])
        return df
    def mask_iso_continent(self, df):
        df['iso_code'] = df['iso_code'].apply(lambda x : 3166)
        df['continent'] = df['continent'].apply(lambda x : 142)
        return df
    def run(self) -> pd.DataFrame:
        df = self.get_df()
        df = self.get_only_tha(df)
        df = self.mask_values(df)
        df = self.drop_columns(df)
        df = self.change_specific_values(df)
        df = self.mask_total_vaccination_values(df)
        df = self.update_latest(df)
        df = self.fill_na(df)
        df = self.extract_date(df)
        df = self.mask_iso_continent(df)
        return df
        