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
            'excess_mortality_cumulative_per_million',
            'new_cases_smoothed',
            'new_vaccinations_smoothed',
            'new_deaths_smoothed',
            'new_deaths_smoothed_per_million',
            'total_cases_per_million',
            'new_cases_per_million',
            'new_cases_smoothed_per_million',
            'total_deaths_per_million',
            'new_deaths_per_million',
            'total_tests_per_thousand',
            'new_tests_per_thousand',
            'new_tests_smoothed',
            'new_tests_smoothed_per_thousand',
            'total_vaccinations_per_hundred',
            'people_vaccinated_per_hundred',
            'people_fully_vaccinated_per_hundred',
            'total_boosters_per_hundred',
            'new_vaccinations_smoothed_per_million',
            'new_people_vaccinated_smoothed',
            'new_people_vaccinated_smoothed_per_hundred',
            'iso_code',
            'location',
            'continent'
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
    def fill_na_people_vaccinated(self, df):
        for j in range(0, 451):
            df.at[j, 'people_vaccinated'] = 0
        df.at[452, 'people_vaccinated'] = (df.iloc[451]['people_vaccinated'] + df.iloc[453]['people_vaccinated']) / 2
        df.at[466, 'people_vaccinated'] = (df.iloc[465]['people_vaccinated'] + df.iloc[467]['people_vaccinated']) / 2
        df.at[496, 'people_vaccinated'] = (df.iloc[495]['people_vaccinated'] + df.iloc[498]['people_vaccinated']) / 2
        df.at[497, 'people_vaccinated'] = (df.iloc[495]['people_vaccinated'] + df.iloc[498]['people_vaccinated']) / 2
        df.at[515, 'people_vaccinated'] = (df.iloc[514]['people_vaccinated'] + df.iloc[516]['people_vaccinated']) / 2
        df.at[588, 'people_vaccinated'] = (df.iloc[587]['people_vaccinated'] + df.iloc[589]['people_vaccinated']) / 2
        df.at[605, 'people_vaccinated'] = (df.iloc[604]['people_vaccinated'] + df.iloc[606]['people_vaccinated']) / 2
        mean = (df.iloc[627]['people_vaccinated'] + df.iloc[640]['people_vaccinated']) / 2
        for j in range(628, 640):
            df.at[j, 'people_vaccinated'] = mean
        df.at[685, 'people_vaccinated'] = (df.iloc[684]['people_vaccinated'] + df.iloc[686]['people_vaccinated']) / 2
        df.at[696, 'people_vaccinated'] = (df.iloc[695]['people_vaccinated'] + df.iloc[697]['people_vaccinated']) / 2
        df.at[943, 'people_vaccinated'] = 42088
        return df
    def fill_na_new_deaths(self, df):
        for j in range(0, 57):
            df.at[j, 'new_deaths'] = 0
        df.at[869, 'new_deaths'] = 31
        return df
    def fill_na_total_deaths(self, df):
        df['total_deaths'] = df['total_deaths'].fillna(0)
        return df
    def fill_na_reproduction_rate(self, df):
        for j in range(0, 72):
            df.at[j, 'reproduction_rate'] = 1
        df.at[942, 'reproduction_rate'] = 1
        df.at[943, 'reproduction_rate'] = 1
        return df
    def fill_na_total_tests(self, df):
        df.at[3, 'total_tests'] = df.iloc[4]['total_tests'] - df.iloc[2]['total_tests']
        for j in range(883, 944):
            df.at[j, 'total_tests'] = df.iloc[j]['total_cases']
        return df
    def fill_na_new_tests(self, df):
        df.at[3, 'new_tests'] = (df.iloc[4]['new_tests'] + df.iloc[2]['new_tests']) / 2
        for x in range(883, 944):
            df.at[x, 'new_tests'] = df.iloc[x]['new_cases']
        return df
    def fill_na_positive_rate(self, df):
        for j in range(0, 24):
            df.at[j, 'positive_rate'] = 0
        df.at[200, 'positive_rate'] = df.iloc[200]['total_tests'] / df.iloc[200]['total_cases']
        for x in range(883, 944):
            df.at[x, 'positive_rate'] = df.iloc[x]['total_tests'] / df.iloc[x]['total_cases']
        return df
    def fill_na_tests_per_case(self, df):
        for j in range(0, 24):
            df.at[j, 'tests_per_case'] = 0
        mean_fifty_first = np.mean([df.iloc[50]['tests_per_case'], df.iloc[52]['tests_per_case']])
        df.at[51, 'tests_per_case'] = mean_fifty_first
        mean_two_hundreds = np.mean([df.iloc[201]['tests_per_case'], df.iloc[199]['tests_per_case']])
        df.at[200, 'tests_per_case'] = mean_two_hundreds
        mean_all = np.mean(df['tests_per_case'])
        for x in range(883, 944):
            df.at[x, 'tests_per_case'] = mean_all
        return df
    def fill_na_people_fully_vacc(self, df):
        before_eighty = 5862
        mean_before_eighty = (29064 - 5862)/80
        total = 5862
        for j in range(0, 445):
            df.at[j, 'people_fully_vaccinated'] = 0
        for x in range(446, 451):
            total += mean_before_eighty
            df.at[x, 'people_fully_vaccinated'] = total
        df.at[452, 'people_fully_vaccinated'] = (df.iloc[453]['people_fully_vaccinated'] - df.iloc[451]['people_fully_vaccinated']) + df.iloc[451]['people_fully_vaccinated']
        df.at[466, 'people_fully_vaccinated'] = (df.iloc[467]['people_fully_vaccinated'] - df.iloc[465]['people_fully_vaccinated']) + df.iloc[465]['people_fully_vaccinated']
        df.at[496, 'people_fully_vaccinated'] = ((df.iloc[498]['people_fully_vaccinated'] - df.iloc[495]['people_fully_vaccinated']) / 2) + df.iloc[495]['people_fully_vaccinated']
        df.at[497, 'people_fully_vaccinated'] = ((df.iloc[498]['people_fully_vaccinated'] - df.iloc[495]['people_fully_vaccinated']) / 2) + df.iloc[496]['people_fully_vaccinated']
        df.at[515, 'people_fully_vaccinated'] = (df.iloc[516]['people_fully_vaccinated'] - df.iloc[514]['people_fully_vaccinated']) + df.iloc[514]['people_fully_vaccinated']
        df.at[588, 'people_fully_vaccinated'] = (df.iloc[589]['people_fully_vaccinated'] - df.iloc[587]['people_fully_vaccinated']) + df.iloc[587]['people_fully_vaccinated']
        df.at[605, 'people_fully_vaccinated'] = (df.iloc[606]['people_fully_vaccinated'] - df.iloc[604]['people_fully_vaccinated']) + df.iloc[604]['people_fully_vaccinated']
        df.at[628, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[627]['people_fully_vaccinated']
        df.at[629, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[628]['people_fully_vaccinated']
        df.at[630, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[629]['people_fully_vaccinated']
        df.at[631, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[630]['people_fully_vaccinated']
        df.at[632, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[631]['people_fully_vaccinated']
        df.at[633, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[632]['people_fully_vaccinated']
        df.at[634, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[633]['people_fully_vaccinated']
        df.at[635, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[634]['people_fully_vaccinated']
        df.at[636, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[635]['people_fully_vaccinated']
        df.at[637, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[636]['people_fully_vaccinated']
        df.at[638, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[637]['people_fully_vaccinated']
        df.at[639, 'people_fully_vaccinated'] = ((df.iloc[640]['people_fully_vaccinated'] - df.iloc[627]['people_fully_vaccinated']) / 12) + df.iloc[638]['people_fully_vaccinated']
        df.at[685, 'people_fully_vaccinated'] = (df.iloc[686]['people_fully_vaccinated'] - df.iloc[684]['people_fully_vaccinated']) + df.iloc[684]['people_fully_vaccinated']
        df.at[696, 'people_fully_vaccinated'] = (df.iloc[697]['people_fully_vaccinated'] - df.iloc[695]['people_fully_vaccinated']) + df.iloc[695]['people_fully_vaccinated']
        df.at[943, 'people_fully_vaccinated'] = 53558583
        return df
    def fill_na_total_boosters(self, df):
        for j in range(0, 640):
            df.at[j, 'total_boosters'] = 0
        df.at[685, 'total_boosters'] = (df.iloc[686]['total_boosters'] - df.iloc[684]['total_boosters']) + df.iloc[684]['total_boosters']
        df.at[696, 'total_boosters'] = (df.iloc[697]['total_boosters'] - df.iloc[695]['total_boosters']) + df.iloc[695]['total_boosters']
        df.at[943, 'total_boosters'] = 31187653
        return df
    def fill_na_stringency_index(self, df):
        df['stringency_index'] = df['stringency_index'].fillna(np.mean(df['stringency_index']))
        return df
    def fill_na_new_vacc(self, df):
        for j in range(0, 641):
            df.at[j, 'new_vaccinations'] = 0
        mean = np.mean([df.iloc[684]['new_vaccinations'], df.iloc[687]['new_vaccinations']])
        df.at[685, 'new_vaccinations'] = mean
        df.at[686, 'new_vaccinations'] = mean
        mean_2 = np.mean([df.iloc[695]['new_vaccinations'], df.iloc[698]['new_vaccinations']])
        df.at[696, 'new_vaccinations'] = mean_2
        df.at[697, 'new_vaccinations'] = mean_2
        df.at[943, 'new_vaccinations'] = 42088
        return df
    def extract_date(self, df):
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df = df.drop(columns=['date'])
        df.rename({"day" : 'date'})
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
        fill_na_people_vaccinated = self.fill_na_people_vaccinated(na_filled_new_cases)
        na_filled_new_deaths = self.fill_na_new_deaths(fill_na_people_vaccinated)
        na_filled_total_deaths = self.fill_na_total_deaths(na_filled_new_deaths)
        na_filled_reproduction_rate = self.fill_na_reproduction_rate(na_filled_total_deaths)
        na_filled_total_cases = self.fill_na_total_tests(na_filled_reproduction_rate)
        na_filled_new_tests = self.fill_na_new_tests(na_filled_total_cases)
        na_filled_positive_rate = self.fill_na_positive_rate(na_filled_new_tests)
        na_filled_tests_per_case = self.fill_na_tests_per_case(na_filled_positive_rate)
        na_filled_people_fully_vac = self.fill_na_people_fully_vacc(na_filled_tests_per_case)
        na_filled_total_boosters = self.fill_na_total_boosters(na_filled_people_fully_vac)
        na_filled_stringency_index = self.fill_na_stringency_index(na_filled_total_boosters)
        na_filled_new_vacc = self.fill_na_new_vacc(na_filled_stringency_index)
        df = self.extract_date(na_filled_new_vacc)
        print(df.columns)
        return df