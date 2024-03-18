import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import pandas as pd
import numpy as np

import database
from database.db_connection import Database
from dabase_df import database_df

import tensorflow
from tensorflow.keras import layers, models


def neural_network(data = database_df()):

    shuffled_df = data.sample(frac=1, random_state=42)
    #ADICIONAR RELATY_PRICE QUE TAVA DANDO ERRO
    #PEGAR 70% DA DATA PARA TREINAR
    X_train = shuffled_df.iloc[1:28000, :].drop(columns= 15)
    print(X_train)
    y_train = shuffled_df.iloc[1:28000, 15]
    print(y_train)
    #PEGAR 15% DA DATA PARA VALIDACAO
    X_val = shuffled_df.iloc[28000:32000, :].drop(columns= 15)
    y_val = shuffled_df.iloc[28000:32000, 15]
    #PEGAR 15% DA DATA PARA TESTE
    X_test = shuffled_df.iloc[32000:35366, :].drop(columns= 15)
    y_test = shuffled_df.iloc[32000:35366, 15]

    X_train = X_train.to_numpy()
    y_train = y_train.to_numpy()

    X_val = X_val.to_numpy()
    y_val = y_val.to_numpy()

    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()

    num_features = 314

    print('Comeco treinamento!!')
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


print('comeco')
neural_network()
