import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from deep_translator import GoogleTranslator
from database.db_connection import Database
import gensim.downloader as api
import pandas as pd 

import time

nltk.download('stopwords')
nltk.download('punkt')
print('Download...')
model = api.load('word2vec-google-news-300')
print('Donload Concluido!')

def convert_data_description(text, model):
    if text is None:
        return None 

    stop_words = set(stopwords.words('english'))
    try:
        translator = GoogleTranslator(source='pt', target='en')
        translated_text = translator.translate(text)
    except:
        translated_text = 'Cannot translate description'

    tokens = word_tokenize(translated_text.lower())
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    word_vectors = []
    i = 0
    word_vectors_error = [0] * 300
    for word in filtered_tokens:
        if word in model.key_to_index:  
            word_vectors.append(model[word])
            
            i += 1
    if word_vectors:
        average_vector = np.mean(word_vectors, axis=0)
    else:
        average_vector = np.array(word_vectors_error)

    try:
        return average_vector
    except:
        print('Erro grave na traducao')

def database_df():
    global database
    
    database = Database()
    response = database.query("""
        SELECT
        r.realty_id,
        r.realty_square_footage,
        r.realty_parking_spaces,
        r.realty_bathrooms,
        r.realty_bedrooms,
        r.realty_advertiser,
        r.realty_status,
        r.realty_furnished,
        r.realty_type,
        r.realty_floor,
        r.realty_condo_price,
        r.realty_property_tax,
        s.street_id,
        ci.city_id,
        n.neighborhood_id,
        r.realty_price,
        r.realty_description

        FROM public.realties r

        INNER JOIN public.streets s ON r.realty_street = s.street_id
        INNER JOIN public.neighborhoods n ON s.street_neighborhood = n.neighborhood_id
        INNER JOIN public.cities ci ON n.neighborhood_city = ci.city_id

        ORDER BY realty_id 
        """)
    i = 0
    for element in response:
        i += 1
        if element[7] == True:
            element[7] = 1
        else:
            element[7] = 0
        result = database.query(
            "SELECT desc_id FROM ai.realty_descriptions"
        )
        if [element[0]] not in result:
            try:
                converted_description = convert_data_description(element[-1], model)
            except:
                converted_description = np.array([0]*300)
            element.pop(-1)
            realty_avarege_description = []


            for number in converted_description:
                realty_avarege_description.append(float(number))
                
            realty_avarege_description_tuple = (element[0], realty_avarege_description)
            insert_df(realty_avarege_description_tuple)
            print(f"Etapa concluida {i}")
            '''data_description_translated = database.query(

                SELECT 
                desc_avg_vector 
                FROM
                ai.realty_descriptions
                ORDER BY desc_id ASC 

                                                )
            print(data_description_translated)'''
        else:
            print("Description already converted and stored.")

    realties_df = pd.DataFrame(response)
    print('Translated with sucsess!!')
    return realty_avarege_description_tuple, realties_df

def insert_df(data):
    realty_id, avg_vector = data
    database.execute(
        "INSERT INTO ai.realty_descriptions (desc_avg_vector, desc_realty) VALUES (%s, %s)",
        (avg_vector, realty_id)
    )
    database.commit()


database_df()