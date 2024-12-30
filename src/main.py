from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

# Load model
model = joblib.load('src/xgboost_model.pkl')

# Definisi aplikasi
app = FastAPI()

# Schema untuk input data
class PricePredictionInput(BaseModel):
    area: float
    harvest_time: int
    harvest_yield: float
    demand: int
    supply: int
    sale: int
    day: int

@app.post("/predict/")
def predict(data: PricePredictionInput):
    input_data = [[
        data.area,
        data.harvest_time,
        data.harvest_yield,
        data.demand,
        data.supply,
        data.sale,
        data.day,
    ]]
    prediction = model.predict(input_data)[0]  # Ambil prediksi pertama
    return {"predicted_price": float(prediction)}  # Konversi ke float
