import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import pandas as pd
import numpy as np

import database
from database.db_connection import Database
from dabase_df import database_df, df

from tensorflow.keras import layers, models
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler

def neural_network(data = df()):
    pd.set_option('display.max_seq_items', None)
    shuffled_df = data.sample(frac=1, random_state=42)
    df_format = shuffled_df.shape
    df_lenght = df_format[0]
    df_col = df_format[1]

    # Divisão dos dados IMPORTANTE GENERALIZAR A DIVISAO USANDO O SHAPE
    '''X_train = shuffled_df.iloc[1:int(df_lenght*0.7), :].drop(columns=16)
    y_train = shuffled_df.iloc[1:int(df_lenght*0.7), 16]
    X_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), :].drop(columns=16)
    y_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), 16]
    X_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, :].drop(columns=16)
    y_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, 16]'''

    X_train = shuffled_df.iloc[1:int(df_lenght*0.7), :]
    y_train = shuffled_df.iloc[1:int(df_lenght*0.7), 15].drop(columns=15)
    X_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), :].drop(columns=15)
    y_val = shuffled_df.iloc[int(df_lenght*0.7):int(df_lenght*0.85), 15]
    X_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, :].drop(columns=15)
    y_test = shuffled_df.iloc[int(df_lenght*0.85):df_lenght, 15]

    X_train = X_train.to_numpy()
    y_train = y_train.to_numpy()
    X_val = X_val.to_numpy()
    y_val = y_val.to_numpy()
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()

    X_train = X_train.astype(np.float32)
    y_train = y_train.astype(np.float32)
    X_val = X_val.astype(np.float32)
    y_val = y_val.astype(np.float32)
    X_test = X_test.astype(np.float32)
    y_test = y_test.astype(np.float32)
    # Normalização dos dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    num_features = X_train.shape[1]-1

    print(f"------Training began with data.shape = {X_train.shape}------".center(100))
    #num_features = 316
    
    model = models.Sequential([
        layers.Input((num_features,)),
        layers.Dense(4096, activation='elu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.5),
        layers.Dense(16384, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.4),
        layers.Dense(16384, activation='elu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.3),
        layers.Dense(8192, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.2),
        layers.Dense(4096, activation='elu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        layers.Dropout(0.1),
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


neural_network()
