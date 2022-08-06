from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
class Data:
    vaccinated : int
    population : int
    
app = FastAPI()

@app.post('/get_new_death_predicted_number')
def get_new_death(data : Data):
    model = joblib.load('new_death_prediction.pkl')
    ratio = data.population / data.vaccinated
    result = model.predict(np.array([ratio]).reshape(1, -1))
    return result[0][0]