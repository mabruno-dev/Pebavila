from gensim.models import KeyedVectors
import gensim.downloader as api

# Carregar seu modelo FastText
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import numpy as np

from data_query import bring_description
from googletrans import Translator, LANGUAGES

translator = Translator()

# Texto de descrição do imóvel
texts = bring_description('realty_description', 'realties')
# Modelo
model = api.load('word2vec-google-news-300')
# Pré-processamento
for text in texts:
    tokens = word_tokenize((translator.translate(text[0], src='pt', dest='en').text).lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]


    word_vectors = []
    for word in filtered_tokens:
        # Supondo que 'model' é o seu modelo Word2Vec carregado
        if word in model.key_to_index:
             word_vectors.append(model[word])
        # Simulação com vetores aleatórios # 300 é uma dimensão comum para embeddings de palavras

    # Calcular a média dos vetores, se houver vetores disponíveis
    if word_vectors:
        average_vector = np.mean(word_vectors, axis=0)
        print("Vetor médio da descrição:", average_vector)
    else:
        print("Nenhuma palavra encontrada nos embeddings.")

