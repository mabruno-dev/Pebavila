import json
from re import findall
from unidecode import unidecode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import RealtyConstants as RC

def find_numbers(s: str):
    result = findall(r"\d+\.*\d*", s)
    # O padrão de expressão regular r'\d+\.*\d*' corresponde a um ou mais dígitos \d+,
    # seguido de um ponto opcional \.* e zero ou mais dígitos \d*.
    # Este padrão permite corresponder a números inteiros e decimais.
    return result if len(result) > 0 else [None]
    
def is_number(s: str):
    return s.isdigit()

def scrape_realty(url):

    driver = webdriver.Chrome()
    driver.get(url)

    # Sugerir troca de realty_done para realty_status
    try:
        status_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main__labels"))
        )
    except:
        print("Connection error")
        driver.quit()
        return scrape_realty(url)

    if "Em construção" in status_span.text:
        status = RC.UNDER_CONSTRUCTION
    elif "Na planta" in status_span.text:
        status = RC.FLOOR_PLAN
    else:
        status = RC.DONE

    # type é uma palavra reservada
    type = unidecode(driver.find_element(By.CLASS_NAME,  "info__business-type").text.split("para")[0].strip().upper())

    location_button = driver.find_element(By.CLASS_NAME, "info__map-link")
    location_list = location_button.text.replace("pin", "").split(",")
    aux = list()
    for item in location_list:
        aux2 = item.split("-")
        for item2 in aux2:
            aux.append(unidecode(item2.strip().upper()))
    location_list = aux
    street = location_list[0]
    if is_number(location_list[1]):
        number = location_list[1]
        neighborhood = location_list[2]
        city = location_list[3]
        state = location_list[4]
    else:
        number = None
        neighborhood = location_list[1]
        city = location_list[2]
        state = location_list[3]

    # DEFINIR TRATAMENTO DO CASO "Sob consulta"
    price_div = driver.find_element(By.CLASS_NAME, "prices__container")
    try:
        price = find_numbers(price_div.text.replace(".", ""))[0]

    except:
        print("Price not informed") # Normalmente sob consulta
        price = None
    try:
        price_ul = price_div.find_element(By.TAG_NAME, "ul")
        price_li_list = price_ul.find_elements(By.TAG_NAME, "li")
        for price_li in price_li_list:

            if "condomínio" in price_li.text:
                condo_price = find_numbers(price_li.text)[0]
            else:
                print("Condo price not informed")
                condo_price = None

            if "IPTU" in price_li.text:
                property_tax = find_numbers(price_li.text)[0]
            else:
                print("Taxes not informed")
                property_tax = None
    except:
        print("Condo price and taxes not informed")
        condo_price = None
        property_tax = None

    # Coleta os valores mais baixos
    features_ul = driver.find_element(By.CLASS_NAME, "info__base-amenities")
    try:
        square_footage = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorSize"]').text)[0]
    except:
        print("Square footage not informed")
        square_footage = None
    try:
        bedrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfRooms"]').text)[0]
    except:
        print("Number of not informed")
        bedrooms = None
    try:
        parking_spaces = find_numbers(features_ul.find_element(By.CLASS_NAME, "js-parking-spaces").text)[0]
    except:
        print("Number of parking spaces not informed")
        parking_spaces = None
    try:
        bathrooms = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="numberOfBathroomsTotal"]').text)[0]
    except:
        print("Number of bathrooms not informed")
        bathrooms = None
    try:
        floor = find_numbers(features_ul.find_element(By.CSS_SELECTOR, 'span[itemprop="floorLevel"]').text)[0]
    except:
        print("Floor not informed")
        floor = None

    # Sugerir mudança de real_state_office para advertiser 
    # e criação de nova tabela advertiser contendo nome e número do anunciante ou utilizacao do creci 
    # (acho que com o creci nao precisa de outra tabela e facilita pois deve ser padrao em todos os sites)
    advertiser_div = driver.find_element(By.CLASS_NAME, "advertser-info--wrapper")
    advertiser_name = unidecode(advertiser_div.find_element(By.CLASS_NAME, "advertiser-info__name").text.strip().upper())
    advertiser_number = advertiser_div.find_element(By.CLASS_NAME, "advertiser-info__offer-codes--advertiser").text.replace("No anunciante:", "").strip() 
    # Não deve ser "unidecodado" e nem capitalizado pois alguns se diferenciam por letras maiusculas e minusculas

    # Descrição deve ser conservada para exibição ao usuário caso necessária
    description = driver.find_element(By.CLASS_NAME, "amenities__description").text.strip()

    if "mobiliado" in url:
        furnished = RC.FURNISHED
    else:
        furnished = RC.NOT_FURNISHED

    realty_dict = {
        "realty_location": {
            "state": state,
            "city": city,
            "neighborhood": neighborhood,
            "street": street
        },
        "realty_number": number,
        "realty_square_footage": square_footage,
        "realty_price": price,
        "realty_description": description,
        "realty_parking_spaces": parking_spaces,
        "realty_bathrooms": bathrooms,
        "realty_bedrooms": bedrooms,
        "realty_real_state_office": advertiser_name,
        "realty_advertiser_number": advertiser_number,
        "realty_done": status,
        "realty_property_tax": property_tax,
        "realty_furnished": furnished,
        "realty_condo_price": condo_price,
        "realty_floor": floor,
        "realty_type": type
    }

    print(f"{json.dumps(realty_dict, indent=4, ensure_ascii=False)}\n")

    return realty_dict