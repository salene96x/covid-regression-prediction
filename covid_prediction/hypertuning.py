from new_etl import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np
class Tuning:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.covid_etl = covid_etl('/usr/src/covid_prediction/our-world-in-data-covid19-dataset/owid-covid-data.csv')
        self.df = self.covid_etl.do()
        self.x_train, self.x_test, self.y_train, self.y_test = self.split_data(self.df)
        self.y_train, self.y_test = self.y_train.to_numpy().reshape(-1), self.y_test.to_numpy().reshape(-1)
    def split_data(self, df):
        x_train, x_test, y_train, y_test = train_test_split(df[["total_cases", "new_cases", "total_deaths",
       "reproduction_rate", "total_tests", "new_tests", "positive_rate",
       "tests_per_case", 'tests_units', 'total_vaccinations',
       'people_vaccinated', 'people_fully_vaccinated', 'total_boosters',
       'new_vaccinations', 'stringency_index', 'population',
       'population_density', 'median_age', 'aged_65_older', 'aged_70_older',
       'gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate',
       'diabetes_prevalence', 'female_smokers', 'male_smokers',
       'handwashing_facilities', 'hospital_beds_per_thousand',
       'life_expectancy', 'human_development_index', 'year', 'month', 'day']], df['new_deaths'], test_size=0.3, random_state=666)
        return x_train, x_test, y_train, y_test                                                    
    def random_search_fit(self, model):
        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
        # Number of features to consider at every split
        max_features = ['auto', 'sqrt', 'log2']
        # Maximum numgt78ber of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4]
        # Method of selecting samples for training each tree
        bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}
        rf_random = RandomizedSearchCV(estimator = model, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = 8)
        # Fit the random search model
        rf_random.fit(self.x_train, self.y_train)
                                                            
        print(rf_random.best_params_)
        return rf_random.best_estimator_
    def evaluate(self, model):
        r2 = r2_score(self.y_test, self.model.predict(self.x_test))
        mae = mean_absolute_error(self.y_test, self.model.predict(self.x_test))
        mse = mean_squared_error(self.y_test, self.model.predict(self.x_test))
        return r2, mae, mse
    def fit(self, x_train, y_train):
        _best_params = self.random_search_fit(self.model)
        self.model = RandomForestRegressor(n_estimators=_best_params['n_estimators'],
                                          max_features=_best_params['max_features'],
                                          max_depth=_best_params['max_depth'],
                                          min_samples_split=_best_params['min_samples_split'],
                                          min_samples_leaf=_best_params['min_samples_leaf'],
                                          bootstrap=_best_params['bootstrap'])
        self.model.fit(x_train, y_train)
        r2, mae, mse = self.evaluate(self.model)
        
class Benchmark(Tuning):
    def __init__(self):
        super().__init__()
    def random_search(self, x_train, y_train):
        best_estimator = self.random_search_fit(self.model)
        self.model = best_estimator
        self.model.fit(x_train, y_train)
        r2, mae, mse = self.evaluate(self.model)
        #print(f"Random Search Based => {r2}, {mae}, {mse}")
        return (r2, mae, mse)
    def grid_search(self, x_train, y_train):
        param_grid = {
    'bootstrap': [True, False],
    'max_depth': [*[item for item in range(10, 120, 10)]],
    'max_features': [None, 'sqrt', 'log2', int(self.df.shape[1] / 3)],
    'min_samples_leaf': [*[item for item in range(1, 20, 1)]],
    'min_samples_split': [*[item for item in range(2, 10)]],
    'n_estimators': [*[item for item in range(100, 2200, 100)]]
}
        model = RandomForestRegressor()
        grid_search = GridSearchCV(estimator = model, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)
        grid_search.fit(self.x_train, self.y_train)
        self.model = grid_search.best_estimator_
        (r2, mae, mse) = self.evaluate(self.model)
        
        #print(f'GridSearchCV => {r2}, {mae}, {mse}')
        return (r2, mae, mse)
    def base_model(self, x_train, y_train):
        rf = RandomForestRegressor()
        rf.fit(x_train, y_train, **fit_param)
        (r2, mae, mse) = self.evaluate(rf)
        return (r2, mae, mse)
    def fit_benchmark(self, x_train, y_train):
        #random_search_metrics = self.random_search(x_train, y_train)
        grid_search_metrics = self.grid_search(x_train, y_train)
        base_model_metrics = self.base_model(x_train, y_train)
        print(base_model_metrics)
        print(grid_search_metrics)
if __name__ == '__main__':
    tuner = Benchmark()
    tuner.fit_benchmark(tuner.x_train, tuner.y_train)