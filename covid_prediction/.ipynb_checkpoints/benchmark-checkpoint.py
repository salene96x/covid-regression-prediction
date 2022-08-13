from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
#from sklearn.catboost import CatBoostRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import LinearRegression
from xgboost.sklearn import XGBRegressor
#from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from new_etl import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
class training:
    def __init__(self, config, model_name):
        self.model_name = model_name
        self.config = config
        self.model = self.get_model()
        self.df = self.get_df()
        self.df_x = self.get_x()
        self.df_y = self.get_y()
    def get_model(self):
        if self.model_name == 'BayesianRidge':
            return BayesianRidge
        elif self.model_name == 'CatBoost':
            return CatBoostRegressor()
        elif self.model_name == 'KernelRidge':
            return KernelRidge()
        elif self.model_name == 'Linear':
            return LinearRegression()
        elif self.model_name == 'XG':
            return XGBRegressor()
        elif self.model_name == 'LGBM':
            return LGBMRegressor()
        elif self.model_name == 'GBR':
            return GradientBoostingRegressor()
        elif self.model_name == 'SVR':
            return SVR()
        elif self.model_name == 'ElasticNet':
            return ElasticNet()
        elif self.model_name == 'SGD':
            return SGDRegressor()
        else:
            return RandomForestRegressor()
        #return models[self.config['MODEL']['MODELTYPE']]
    def train(self, x_train, y_train):
        self.model.fit(x_train, y_train)
    def split_data(self):
        x_train, x_test, y_train, y_test = train_test_split(self.df_x, self.df_y, test_size=0.3, random_state=66)
        return x_train, x_test, y_train, y_test
    def scaled_data(self):
        x_train, x_test, y_train, y_test = self.split_data()
        scaler_x = StandardScaler()
        scaler_y = StandardScaler()
        
        x_train = scaler_x.fit_transform(x_train)
        x_test = scaler_x.transform(x_test)
        
        y_train = scaler_y.fit_transform(y_train)
        y_test = scaler_y.transform(y_test)
        return x_train, x_test, y_train, y_test, scaler_y
    def get_x(self):
        x_df = self.df.drop(columns=self.config['DATASET']['Y']).copy()
        x = self.df[self.config['DATASET']['X']]
        return x
    def get_y(self):
        y = self.df[self.config['DATASET']['Y']]
        return y
    def get_df(self):
        etl = covid_etl(self.config["DATASET"]['PATH'])
        df = etl.do()
        return df
    def run(self):
        x_train, x_test, y_train, y_test, scaler_y = self.scaled_data()
        self.train(x_train, y_train)
        return self.model