from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from new_etl import *
import yaml
import sys
import json

class training:
    def __init__(self, config):
        self.config = config
        self.model = self.get_model()
        self.df = self.get_df()
        self.df_x = self.get_x()
        self.df_y = self.get_y()
    def get_model(self):
        
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
        return self.model, x_test, y_test, scaler_y
    

#if len(sys.argv) == 0:
    #print("Missing CONFIG FILE'S name!")
    #sys.exit()
#try:
    #ymlfile = open(sys.argv[0], 'r')
#except:
    #print("NO FILES GIVEN")
#with open('test-config.json') as json_file:
    #cfg = json.load(json_file)
#with open('regression-training-ex-1.yaml', 'r') as yml_file:
    #cfg = confuse.Configuration("regression-training-ex-1", __name__)
#print(type(cfg['MODEL']['MODELTYPE']))
#trainer = training(cfg['DATASET']['PATH'])
#model = trainer.run()
#print("Successfully trained")