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

global database
database = Database()
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
    nltk.download('stopwords')
    nltk.download('punkt')
    print('Download...')
    model = api.load('word2vec-google-news-300')
    print('Donload Concluido!')
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

    print('Translated with sucsess!!')

def insert_df(data):
    realty_id, avg_vector = data
    database.execute(
        "INSERT INTO ai.realty_descriptions (desc_avg_vector, desc_realty) VALUES (%s, %s)",
        (avg_vector, realty_id)
    )
    database.commit()

def create_df():
    data_description_translated = database.query('''

                SELECT 
                desc_avg_vector, desc_realty
                FROM
                ai.realty_descriptions
                ORDER BY desc_realty ASC 

                                                ''')
    temporary_list_2 = []
    for element in data_description_translated:
        temporary_list = []
        for element_2 in element[0]:
            temporary_list.append(float(element_2))
        temporary_list.append(element[1])
        temporary_list_2.append(temporary_list)
    df = pd.DataFrame(temporary_list_2)
    return df

def df():
    df = create_df()

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
            r.realty_price

            FROM public.realties r

            INNER JOIN public.streets s ON r.realty_street = s.street_id
            INNER JOIN public.neighborhoods n ON s.street_neighborhood = n.neighborhood_id
            INNER JOIN public.cities ci ON n.neighborhood_city = ci.city_id


            ORDER BY realty_id 
            """)
        
    df_2 = pd.DataFrame(response)
    '''resultado = pd.merge(df_2, df, left_on=df_2.columns[0], right_on=df.columns[300], how='right')

    if (resultado.iloc[:, 1] == resultado.iloc[:, -1]).all():
        resultado = resultado.drop(columns=[resultado.columns[-1]])
        print("DATA FETCHED WITH SUCSESS:".center(100))
    else:
        print(resultado.iloc[:,-1])
    resultado.rename(columns={'key_0': 0, '0_x': 1, '1_x': 2, '2_x': 3, '3_x': 4, '4_x': 5, '5_x': 6, '6_x': 7, '7_x': 8, '8_x': 9, '9_x': 10, '10_x': 11, '11_x': 12, '12_x': 13, '13_x': 14, '14_x': 15, '15_x': 16, '0_y': 17, '1_y': 18, '2_y': 19, '3_y': 20, '4_y': 21, '5_y': 22, '6_y': 23, '7_y': 24, '8_y': 25, '9_y': 26, '10_y': 27, '11_y': 28, '12_y': 29, '13_y': 30, '14_y': 31, '15_y': 32, 16: 33, 17: 34, 18: 35, 19: 36, 20: 37, 21: 38, 22: 39, 23: 40, 24: 41, 25: 42, 26: 43, 27: 44, 28: 45, 29: 46, 30: 47, 31: 48, 32: 49, 33: 50, 34: 51, 35: 52, 36: 53, 37: 54, 38: 55, 39: 56, 40: 57, 41: 58, 42: 59, 43: 60, 44: 61, 45: 62, 46: 63, 47: 64, 48: 65, 49: 66, 50: 67, 51: 68, 52: 69, 53: 70, 54: 71, 55: 72, 56: 73, 57: 74, 58: 75, 59: 76, 60: 77, 61: 78, 62: 79, 63: 80, 64: 81, 65: 82, 66: 83, 67: 84, 68: 85, 69: 86, 70: 87, 71: 88, 72: 89, 73: 90, 74: 91, 75: 92, 76: 93, 77: 94, 78: 95, 79: 96, 80: 97, 81: 98, 82: 99, 83: 100, 84: 101, 85: 102, 86: 103, 87: 104, 88: 105, 89: 106, 90: 107, 91: 108, 92: 109, 93: 110, 94: 111, 95: 112, 96: 113, 97: 114, 98: 115, 99: 116, 100: 117, 101: 118, 102: 119, 103: 120, 104: 121, 105: 122, 106: 123, 107: 124, 108: 125, 109: 126, 110: 127, 111: 128, 112: 129, 113: 130, 114: 131, 115: 132, 116: 133, 117: 134, 118: 135, 119: 136, 120: 137, 121: 138, 122: 139, 123: 140, 124: 141, 125: 142, 126: 143, 127: 144, 128: 145, 129: 146, 130: 147, 131: 148, 132: 149, 133: 150, 134: 151, 135: 152, 136: 153, 137: 154, 138: 155, 139: 156, 140: 157, 141: 158, 142: 159, 143: 160, 144: 161, 145: 162, 146: 163, 147: 164, 148: 165, 149: 166, 150: 167, 151: 168, 152: 169, 153: 170, 154: 171, 155: 172, 156: 173, 157: 174, 158: 175, 159: 176, 160: 177, 161: 178, 162: 179, 163: 180, 164: 181, 165: 182, 166: 183, 167: 184, 168: 185, 169: 186, 170: 187, 171: 188, 172: 189, 173: 190, 174: 191, 175: 192, 176: 193, 177: 194, 178: 195, 179: 196, 180: 197, 181: 198, 182: 199, 183: 200, 184: 201, 185: 202, 186: 203, 187: 204, 188: 205, 189: 206, 190: 207, 191: 208, 192: 209, 193: 210, 194: 211, 195: 212, 196: 213, 197: 214, 198: 215, 199: 216, 200: 217, 201: 218, 202: 219, 203: 220, 204: 221, 205: 222, 206: 223, 207: 224, 208: 225, 209: 226, 210: 227, 211: 228, 212: 229, 213: 230, 214: 231, 215: 232, 216: 233, 217: 234, 218: 235, 219: 236, 220: 237, 221: 238, 222: 239, 223: 240, 224: 241, 225: 242, 226: 243, 227: 244, 228: 245, 229: 246, 230: 247, 231: 248, 232: 249, 233: 250, 234: 251, 235: 252, 236: 253, 237: 254, 238: 255, 239: 256, 240: 257, 241: 258, 242: 259, 243: 260, 244: 261, 245: 262, 246: 263, 247: 264, 248: 265, 249: 266, 250: 267, 251: 268, 252: 269, 253: 270, 254: 271, 255: 272, 256: 273, 257: 274, 258: 275, 259: 276, 260: 277, 261: 278, 262: 279, 263: 280, 264: 281, 265: 282, 266: 283, 267: 284, 268: 285, 269: 286, 270: 287, 271: 288, 272: 289, 273: 290, 274: 291, 275: 292, 276: 293, 277: 294, 278: 295, 279: 296, 280: 297, 281: 298, 282: 299, 283: 300, 284: 301, 285: 302, 286: 303, 287: 304, 288: 305, 289: 306, 290: 307, 291: 308, 292: 309, 293: 310, 294: 311, 295: 312, 296: 313, 297: 314, 298: 315, 299: 316}, inplace=True)
    resultado.fillna(resultado.mean(), inplace=True)'''
    df_2.fillna(df_2.mean(), inplace=True)
    return df_2

