import pandas as pd
import numpy as np
class covid_etl:
    def __init__(self, data_path: str):
        self.PATH = data_path
        #self._columns_to_drop = None
    def drop_columns(self, df):
        _columns_to_drop = [
            'icu_patients',
            'icu_patients_per_million',
            'hosp_patients',
            'hosp_patients_per_million',
            'weekly_icu_admissions',
            'weekly_icu_admissions_per_million',
            'weekly_hosp_admissions',
            'weekly_hosp_admissions_per_million',
            'excess_mortality_cumulative_absolute',
            'excess_mortality_cumulative',
            'excess_mortality',
            'excess_mortality_cumulative_per_million'
        ]
        df = df.drop(columns=_columns_to_drop)
        return df
    def merge_total_vacc(self, main_df):
        to_merge = pd.read_csv('/usr/src/covid_prediction/covid-vaccination-dataset/vaccinations.csv')
        to_merge = to_merge.loc[to_merge['location'] == 'Thailand']
        main_df['date'] = pd.to_datetime(main_df['date'], format='%Y-%m-%d')
        to_merge['date'] = pd.to_datetime(to_merge['date'], format='%Y-%m-%d')
        main_df.set_index('date', inplace=True)
        main_df.update(to_merge.set_index('date'))
        main_df = main_df.reset_index()
        return main_df
    def fill_na_total_vacc(self, df):
        for j in range(0, 450):
            df.at[j, 'total_vaccinations'] = 0
        for j in range(628, 639):
            df.at[j, 'total_vaccinations'] = np.mean(df['total_vaccinations'].loc[df['date'] > '2021-10-04'])
        df.at[450, 'total_vaccinations'] = (df.iloc[451]['total_vaccinations'] - df.iloc[449]['total_vaccinations']) + df.iloc[449]['total_vaccinations'] 
        df.at[452, 'total_vaccinations'] = (df.iloc[453]['total_vaccinations'] - df.iloc[451]['total_vaccinations']) + df.iloc[451]['total_vaccinations'] 
        df.at[466, 'total_vaccinations'] = (df.iloc[467]['total_vaccinations'] - df.iloc[465]['total_vaccinations']) + df.iloc[465]['total_vaccinations'] 
        df.at[496, 'total_vaccinations'] = ((df.iloc[498]['total_vaccinations'] - df.iloc[495]['total_vaccinations']) / 2) + df.iloc[495]['total_vaccinations'] 
        df.at[497, 'total_vaccinations'] = ((df.iloc[498]['total_vaccinations'] - df.iloc[495]['total_vaccinations']) / 2) + df.iloc[495]['total_vaccinations']
        df.at[515, 'total_vaccinations'] = (df.iloc[516]['total_vaccinations'] - df.iloc[514]['total_vaccinations'])  + df.iloc[514]['total_vaccinations'] 
        df.at[588, 'total_vaccinations'] = (df.iloc[589]['total_vaccinations'] - df.iloc[587]['total_vaccinations'])  + df.iloc[587]['total_vaccinations'] 
        df.at[605, 'total_vaccinations'] = (df.iloc[606]['total_vaccinations'] - df.iloc[604]['total_vaccinations'])  + df.iloc[604]['total_vaccinations']
        df.at[639, 'total_vaccinations'] = (df.iloc[640]['total_vaccinations'] - df.iloc[638]['total_vaccinations'])  + df.iloc[638]['total_vaccinations'] 
        df.at[685, 'total_vaccinations'] = (df.iloc[686]['total_vaccinations'] - df.iloc[684]['total_vaccinations'])  + df.iloc[684]['total_vaccinations']
        df.at[696, 'total_vaccinations'] = (df.iloc[697]['total_vaccinations'] - df.iloc[695]['total_vaccinations'])  + df.iloc[695]['total_vaccinations'] 
        df.at[943, 'total_vaccinations'] = 141814894
        return df
    def fillna_total_cases(self, df):
        for j in range(0, 18):
            df.at[j, 'total_cases'] = 0
        return df
    def fill_na_tests_units(self, df):
        df['tests_units'] = df['tests_units'].fillna('tests performed')
        return df
    def map_tests_units(self, df):
        df['tests_units'] = np.where(df['tests_units'] =='tests performed', 1, 0)
        return df
    def fill_na_new_cases(self, df):
        for j in range(0, 19):
            df.at[j, 'new_cases'] = 0
        df.at[200, 'new_cases'] = (df.iloc[201]['new_cases'] - df.iloc[199]['new_cases']) + df.iloc[199]['new_cases']
        df.at[869, 'new_cases'] = (df.iloc[870]['new_cases'] - df.iloc[868]['new_cases']) + df.iloc[868]['new_cases']
        return df
    def do(self):
        _df = pd.read_csv(self.PATH)
        _df = _df.loc[_df['location'] == 'Thailand']
        dropped_columns_df = self.drop_columns(_df)
        merged_df = self.merge_total_vacc(dropped_columns_df)
        na_filled_total_vacc_df = self.fill_na_total_vacc(merged_df)
        na_filled_total_cases_df = self.fillna_total_cases( na_filled_total_vacc_df)
        na_filled_tests_units_df = self.fill_na_tests_units(na_filled_total_cases_df)
        mapped_tests_units_df = self.map_tests_units(na_filled_tests_units_df)
        na_filled_new_cases = self.fill_na_new_cases(mapped_tests_units_df)
        df = na_filled_new_cases
        return df