from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
class Data(BaseModel):
    vaccinated : int
    population : int
    
app = FastAPI()

@app.post('/get_new_death_predicted_number')
def get_new_death(data : Data):
    #os.system("cd C:\\Users\\MagicComputer\\Documents\\GitHub\\MLOps-Regression-Machine-Learning-Problem\\Covid-Regression-MortalityVSPopulation\\models")
    model = joblib.load('new_death_prediction.pkl')
    model_ss = joblib.load("StandardScaler_Model.pkl")
    ratio = data.population / data.vaccinated
    result = model_ss.inverse_transform(model.predict(np.array([ratio]).reshape(1, -1)))
    return {"Response" : 
    { 
    "NewDeaths" : int(result[0][0])
    }
    }