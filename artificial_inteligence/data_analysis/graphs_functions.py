import pandas as pd
import json
import matplotlib.pyplot as plt
import sklearn 

# Suponha que `df` seja o seu DataFrame

def enumerate_streets(df, data_dict):
    k = 0
    h = 0
    dict_streets = {}
    # Loop direto sobre a lista de dicionários fornecida
    for item in df['realty_location_street']:
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
            data_dict[h]['realty_location']['street'] = dict_streets[item]
        
        except:
            data_dict[h]['realty_location']['street'] = dict_streets[item]
        
        h += 1

        return dict_streets, data_dict

def enumerate_neighborhoods(df, data_dict):
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
            data_dict[h]['realty_location']['neighborhood'] = dict_neighborhoods[item]
        except:
            data_dict[h]['realty_location']['neighborhood'] = dict_neighborhoods[item]
        
        data_dict[h]['realty_location']['city'] = 1
        data_dict[h]['realty_location']['state'] = 1
        data_dict[h]['realty_url'] = 0
        data_dict[h]['realty_description'] = 0
        data_dict[h]['realty_advertiser'] = 0
        data_dict[h]['realty_advertiser_number'] = 0
        data_dict[h]['realty_type'] = 0

        h += 1

    return dict_neighborhoods, data_dict

def streets():

    file_path = '~/artificial_inteligence/realties.json'

# Abrindo o arquivo JSON e carregando o conteúdo como um dicionário
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
        data_dict = data_dict["realties"]
        df = pd.json_normalize(data_dict, sep = '_')
        #print(data_dict[0:1])
        file.close()

    print(df.iloc[0:20])
    keys = df.keys()

    return df, data_dict

def parametrize_for_IA(data_dict):
    return df

df, data_dict = streets()

dict_streets, data_dict = enumerate_streets(df, data_dict)

dict_neighborhoods, data_dict = enumerate_neighborhoods(df, data_dict)

df_parametrized = parametrize_for_IA(data_dict)

df = pd.json_normalize(data_dict, sep='_')


print(df)




