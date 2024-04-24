from __future__ import division
import numpy as np
import tensorflow as tf
import keras
import os
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def predict():
    model = tf.keras.models.load_model('model.h5')
    ho_chi_minh_df = pd.read_csv('hochiminh.csv')
    scaler = MinMaxScaler()
    rain = ho_chi_minh_df['rain'].values.reshape(-1, 1)
    scaler.fit(rain)

    last_8_rows = ho_chi_minh_df.tail(8)
    input = last_8_rows[['max', 'min', 'averageTemp', 'humidi']].values
    input = input.reshape(1, 8, 4)
     # Convert predictions to a Python list
    predictions = model.predict(input)
    predictions = scaler.inverse_transform(predictions).tolist()
    
    return predictions

