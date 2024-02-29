import os, sys
project_name = "the-beginning"; sys.path.append(os.path.abspath(__file__)[:os.path.abspath(__file__).find(project_name) + len(project_name)] if project_name in os.path.abspath(__file__) else os.path.abspath(__file__))

import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk
from googletrans import Translator, LANGUAGES
import database
from database.db_connection import Database
import gensim.downloader as api

def convert_data_description():
    model = api.load('word2vec-google-news-300')

    database = Database()


    translator = Translator()

    texts = database.query(" SELECT realty_description FROM relaties ")

    stop_words = set(stopwords.words('english'))

    for text in texts:
        translated_text = translator.translate(text[0], src='pt', dest='en').text

        tokens = word_tokenize((translated_text).lower())
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

        word_vectors = []
        for word in filtered_tokens:
            if word in model.key_to_index:  
                word_vectors.append(model[word])

        if word_vectors:
            average_vector = np.mean(word_vectors, axis=0)
            #print("Vetor médio da descrição:", average_vector)
        else:
            print("Nenhuma palavra encontrada nos embeddings.")

    return average_vector


