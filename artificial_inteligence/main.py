import pandas as pd
import json
import matplotlib.pyplot as plt


# Suponha que `df` seja o seu DataFrame

def enumerate_streets(df, data_dict):
    k = 0
    h = 0
    dict_streets = {}
    # Loop direto sobre a lista de dicionários fornecida
    for item in df['realty_location_street']:
        print(item)
        # Acessa diretamente 'realty_location' e então 'street'
        
        # Verifica se a rua já existe no dicionário
        if item not in dict_streets:
            dict_streets[item] = k
            k += 1
        else:
            data_dict[h]['realty_location']['street'] = dict_streets[item]


        h+= 1

    h = 0
    for item in df['realty_location_street']:
        # Acessa diretamente 'realty_location' e então 'street'

        try:
            int(item)
        
        except:
            data_dict[h]['realty_location']['street'] = dict_streets[item]
        
        h += 1

        return dict_streets

def enumerate_neiborhoods(df, data_dict):
    k = 0
    h = 0
    dict_neighborhoods = {}
# Loop direto sobre a lista de dicionários fornecida
    for item in df['realty_location_neighborhood']:
        #print(item)
        # Acessa diretamente 'realty_location' e então 'neighborhood'
        
        # Verifica se a rua já existe no dicionário
        if item not in dict_neighborhoods:
            dict_neighborhoods[item] = k
            k += 1
        else:
            data_dict[h]['realty_location']['neighborhood'] = dict_neighborhoods[item]


        h+= 1

    h = 0
    for item in df['realty_location_neighborhood']:
    # Acessa diretamente 'realty_location' e então 'neighborhood'

        try:
            int(item)
        
        except:
            data_dict[h]['realty_location']['neighborhood'] = dict_neighborhoods[item]
        
        h += 1
    
    return dict_neighborhoods

def streets():
    file_path = '/Users/victorhugo/Documents/GitHub/the-beginning/artificial_inteligence/realties.json'

# Abrindo o arquivo JSON e carregando o conteúdo como um dicionário
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
        #print(data_dict[0:1])
        file.close()

    df = pd.json_normalize(data_dict, sep='_')
    return df['realty_location_street']
# Configurar o pandas para exibir todas as linhas
'''pd.set_option('display.max_rows', None)

# Configurar o pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)

# Configurar a largura máxima da coluna para garantir que o pandas não quebre as células
pd.set_option('display.max_colwidth', None)

# Configurar para que o pandas exiba todas as colunas na tela sem truncá-las.
# Isso pode ser útil para DataFrames com muitas colunas.
pd.set_option('display.width', None)

# Caminho para o arquivo JSON
file_path = '/Users/victorhugo/Documents/GitHub/the-beginning/artificial_inteligence/realties.json'

# Abrindo o arquivo JSON e carregando o conteúdo como um dicionário
with open(file_path, 'r') as file:
    data_dict = json.load(file)
    #print(data_dict[0:1])
    file.close()'''


#for 
# Ler o arquivo JSON e criar o DataFrame
'''df = pd.json_normalize(data_dict, sep='_')

dict_neighborhoods = enumerate_neiborhoods(df, data_dict)
dict_streets = enumerate_streets(df, data_dict)
# Imprime o dicionário resultante
print(dict_neighborhoods)

print(dict_streets)
                
print(df.shape)

df.to_excel('dados_zapimoveis.xlsx', sheet_name='Dados', index=False)'''

#print(df)

'''
# Criando o gráfico de barras
plt.bar(x, y)

# Adicionando título e rótulos aos eixos
plt.title('Gráfico de Barras')
plt.xlabel('BAIRRO')
plt.ylabel('RUA')

# Exibindo o gráfico
plt.show()'''


