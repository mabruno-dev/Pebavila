import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import pandas as pd
import numpy as np

import database
from database.db_connection import Database
from dabase_df import database_df

import tensorflow as tf
from tensorflow.keras import layers, models


def neural_network(data = database_df()):

    shuffled_df = data.sample(frac=1, random_state=42)
    #Codigo acima para aleatorizar o dataframe, falta ajeitar resultados NaN dentro dele
    #PEGAR 70% DA DATA PARA TREINAR
    X_train = shuffled_df.iloc[1:, :-2]
    y_train = shuffled_df.iloc[-2:, :] 
    #PEGAR 15% DA DATA PARA VALIDACAO
    X_val = 0
    y_val = 0
    #PEGAR 15% DA DATA PARA TESTE
    X_test = 0
    y_test = 0

#testar no pc q tem acesso ao hamachi 

    num_features = 314

    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(num_features,)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1)) 

    model.compile(optimizer='adam',
                loss='mean_squared_error',
                metrics=['mae']) 
                
    history = model.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val))

    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f'Test Loss: {test_loss}, Test MAE: {test_mae}')

    new_property = ['dados, para previsao'] 
    predicted_price = model.predict([new_property])
    print(f'Predicted Price: {predicted_price}')


