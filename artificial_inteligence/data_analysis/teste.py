from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk
from data_query import bring_description

# Baixe o conjunto de dados stopwords do NLTK, se ainda não o fez


# Carregar um modelo pré-treinado (este é um exemplo, você precisará baixar um modelo real)
# Para este exemplo, estamos usando um caminho fictício; você precisará substituí-lo pelo caminho do seu modelo pré-treinado
# model = KeyedVectors.load_word2vec_format('path/to/your/model/word2vec/GoogleNews-vectors-negative300.bin', binary=True)

# Texto de descrição do imóvel
texts = bring_description('realty_description', 'realties')
# Pré-processamento
for text in texts:
    tokens = word_tokenize(text[0].lower())
    stop_words = set(stopwords.words('portuguese'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    # Extrair embeddings e calcular a média (simulação, já que não temos o modelo carregado)
    # Para este exemplo, geraremos vetores aleatórios para simular os embeddings
    word_vectors = []
    for word in filtered_tokens:
        # Supondo que 'model' é o seu modelo Word2Vec carregado
        # if word in model.vocab:
        #     word_vectors.append(model[word])
        # Simulação com vetores aleatórios
        word_vectors.append(np.random.rand(300))  # 300 é uma dimensão comum para embeddings de palavras

    # Calcular a média dos vetores, se houver vetores disponíveis
    if word_vectors:
        average_vector = np.mean(word_vectors, axis=0)
        print("Vetor médio da descrição:", average_vector)
    else:
        print("Nenhuma palavra encontrada nos embeddings.")

