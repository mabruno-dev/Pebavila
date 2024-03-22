import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import pandas as pd
import numpy as np

import database
from database.db_connection import Database
from dabase_df import database_df

from tensorflow.keras import layers, models
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler

def neural_network(data = database_df()):

    shuffled_df = data.sample(frac=1, random_state=42)
    df_format = shuffled_df.shape
    df_lenght = df_format[1]
    df_col = df_format[0]

    # Divisão dos dados IMPORTANTE GENERALIZAR A DIVISAO USANDO O SHAPE
    X_train = shuffled_df.iloc[1:int(df_lenght*0.7), :].drop(columns=15)
    y_train = shuffled_df.iloc[1:int(df_lenght*0.7), 15]
    X_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), :].drop(columns=15)
    y_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), 15]
    X_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, :].drop(columns=15)
    y_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, 15]

    # Normalização dos dados
    '''scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)'''

    '''num_features = X_train_scaled.shape[1]'''

    num_features = 315
    # Construção do modelo
    model = models.Sequential([
        layers.Dense(128, activation='relu', input_shape=(num_features,), kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(1)
    ])

    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=['mae'])

    # Callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=10)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

    # Treinamento
    history = model.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val), callbacks=[early_stop, reduce_lr])

    # Avaliação
    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f'Test Loss: {test_loss}, Test MAE: {test_mae}')

    # Predição para uma nova propriedade
'''    new_property = np.array(['dados, para previsao'])  # Ajuste esta linha conforme a necessidade de preprocessamento dos novos dados
    new_property_scaled = scaler.transform(new_property.reshape(1, -1))
    predicted_price = model.predict(new_property)
    print(f'Predicted Price: {predicted_price}')'''


print('comeco')
neural_network()
