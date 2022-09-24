import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn
#import selenium
import logging
import os
from new_etl import covid_etl
import yaml

import importlib

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

class Trainer:
    def __init__(self, config):
        self.config = config
        #self.import_status = self.import_modules(self.config['models'])
    def import_modules(self, models):
        #for k,v in models.items():
            #for j in v:
                #importlib.import_module('sklearn')
                #importlib.import_module(f'sklearn.{k}')
                #importlib.import_module(j)
        for k, v in models.items():
            for j in v:
                eval(f"exec('from sklearn.{k} import {j}')")
        return True
    def train(self, models, ex_id):
        #for k, v in models:
            for j in models:
                with mlflow.start_run(experiment_id=ex_id):
                    x_train, y_train, x_test, y_test = self.split_data(self.config)
            #self.train(self.config['models'], x_train, y_train, x_test, y_test) 
                    #print(y_test.shape)
                    model = eval(f'{j}()')
                    #raise ValueError('Pause')
                    model.fit(x_train, y_train)
                    y_pred = model.predict(x_test)
                    rmse, mae, r2 = self.eval_metrics(y_test, y_pred)
                    mlflow.log_metric("rmse", rmse)
                    mlflow.log_metric("r2", r2)
                    mlflow.log_metric("mae", mae)
                    mlflow.end_run()
    def split_data(self, config):
        etl = covid_etl(f'/usr/src/covid_prediction/our-world-in-data-covid19-dataset/owid-covid-data.csv')
        df = etl.do()
        self.df_x = df[config['dataset']['x']]
        self.df_y = df[config['dataset']['y']]
        x_train, x_test, y_train, y_test = train_test_split(self.df_x, self.df_y, test_size=float(config['train_test_split']['test_size']), random_state=int(config['train_test_split']['random_state']))
        std_x = StandardScaler()
        std_y = StandardScaler()
        x_train = std_x.fit_transform(x_train)
        x_test = std_x.transform(x_test)
        y_train = std_y.fit_transform(y_train)
        y_test = std_y.transform(y_test)
        return x_train, y_train, x_test, y_test
    def perform(self):
        try :
            ex_id = mlflow.create_experiment(self.config['experiment_name'])
        except:
            current_experiment = dict(mlflow.get_experiment_by_name(self.config['experiment_name']))
            ex_id = current_experiment['experiment_id']
        self.train(self.config['models'], ex_id)
            
    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
def read_cfg(cfg_name):
    new_path = f'/usr/src/covid_prediction/{cfg_name}'
    with open(new_path, 'r') as yaml_file:
        cfg = yaml.load(yaml_file)
    return cfg

if __name__ == "__main__":
    try :
        cfg = read_cfg(sys.argv[1])
    except:
        raise ValueError('The following variable(s) not provided : \n- EXPERIMENT_NAME')
                                    
    trainer = Trainer(cfg)
    trainer.perform()
    os.system('mlflow server -h 0.0.0.0 -p 5959')
    selenium.get('0.0.0.0:5959')
    print('Successfully train @use \nmlflow server -h 0.0.0.0 -p 5959\nto show ui.')