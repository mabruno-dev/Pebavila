# Importações necessárias para automação web e manipulação de tempo.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def web_scrap(link_fornecido, state):
    # Configure Selenium to use the proxy


    gecko_driver_path = 'geckodriver'  # Update this path
    options = Options()
    # Set up the service object with the path to GeckoDriver
    service = Service(executable_path=gecko_driver_path)

    # Pass the service object to the driver
    driver = webdriver.Firefox(service=service)

    driver.get(link_fornecido)


    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.TAG_NAME, "span"))
    )

    # Here you can specify custom headers via the proxy

    # Espera 5 segundos para garantir que a página tenha carregado completamente.
    # Busca por todos os elementos 'span' na página, que podem conter informações relevantes.
    elements = driver.find_elements(By.TAG_NAME, 'span')

    elements_2 = driver.find_elements(By.TAG_NAME, 'div')



    # Declaracao de variaveis e contadores necessarios
    i = 0
    j = 0
    k = 0
    y = 0
    property_dict = {}
    price_list = []


    # Abre as diferentes paginas do website.
    for element in elements_2:

    #print(f"{element.text}-->{i}")

    # Coleta do No do anunciante
        if "No anunciante" in element.text and k != 1:
            index = element.text.index("No anunciante")
            number = ''.join([caractere for caractere in element.text[index:index+30] if caractere.isdigit()])
            number = element.text[index+15] + number
            k += 1


    # Coleta Nome imobiliaria
        if "denunciar" in element.text and y != 1:
            index = element.text.index("denunciar")
            index2 = element.text.index("Vendas")

            imobiliaria = element.text[index+18:index2] ## ver se vai precisar ajustar tamanho para outras imobiliarias##
            y += 1

    # Coleta descricao do imovel
        if "Características" in element.text:
            index = element.text.index("Características")
            index2 = element.text.index("Mostrar mais")
            descricao = element.text[index:index2]
        

        i += 1
    i = 0


    # Itera pelos elementos 'span' para extrair informações específicas.
    for element in elements:

        #print(f"{element.text}-->{i}")

    # Verifica se o elemento contém informações de preço.
        try:
            if "R$" in element.text:
                index = element.text.index("R$")
                price = ''.join([caractere for caractere in element.text[index:index+30] if caractere.isdigit()])
                price = float(price)
                price_list.append(price)
        except:
            price_list.append('None')
        

    # Verifica se o elemento contém informações de metragem quadrada.
        try:
            if "m²" in element.text:
                if j == 0:
                    meters = ''.join([caractere for caractere in element.text if caractere.isdigit()])
                    meters = float(meters[0:-1])
                j += 1
        except:
            meters = None
            print("No information about square_footage")


    # Determina o tipo de imóvel com base no texto do elemento.
        if "Casa" in element.text:
            realty_type = "house"
        elif "Apartamento" in element.text:
            realty_type = "apartament"
        else:
            realty_type = "building"


    # Extrai informações de localização se o elemento contém um "pin".
        if "pin" in element.text:
            try:
                index = i+1
                loc = elements[index].text[:-3].split()
                neighborhood = elements[index].text[:-3].split('-')[1].split(',')[0]
                public_place = loc[0]
                street = ''
                #bumero = 0
                for n in loc:
                    #if bumero != 0:
                    street += n
                    street += ' '
                    #bumero = 1
                city = street.split(',')[1].split("-")[0]
                street = street.split("-")[0]
            except:
                i+=1
                continue


    # Extrai o número de quartos, vagas de estacionamento e banheiros com base no texto do elemento.
        try:
            if "bedroom" in element.text:
                try:
                    index = i+1
                    loc = elements[index].text.split()
                    bedroom = int(loc[0])
                except:
                    i+=1
                    continue
        except:
            bedroom = None
            print("No information about bedroom")
        try:
            if "parking" in element.text:
                try:
                    index = i+1
                    loc = elements[index].text.split()
                    parking_spot = int(loc[0])
                except:
                    i+=1
                    continue
        except:
            parking_spot = None
            print("No information about parking_spot")


        try:
            if "bathroom" in element.text:
                try:
                    index = i+1
                    loc = elements[index].text.split()
                    bathroom = int(loc[0])
                except:
                    i+=1
                    continue
        except:
            bathroom = None
            print("No information about bathroom")


        if "Na planta" in element.text:
            lancamento = 0
        elif "Em construcao" in element.text:
            lancamento = 1
        else:
            lancamento = 2
        

        i+=1


    # Compila as informações extraídas em um dicionário.
    property_dict = {

        "realty_type": realty_type,
        "realty_square_footage": meters, 
        "realty_property_tax": price_list[0], 
        "realty_price": price_list[1],
        "realty_rent_price": 'not implemented', ##ainda nao implementado##
        "realty_description": descricao,
        "realty_parking_spaces": parking_spot, 
        "realty_bathroom": bathroom, 
        "realty_bedroom": bedroom, 
        "realty_real_state_office": imobiliaria,
        "realty_advertiser_number": number,
        "realty_done": lancamento,
        "location": {
            "city_name": city, 
            "neighborhood_name": neighborhood,
            "street_name": street,
            "state_name": state
                    }


        #"public_place": public_place,          
                }

    # Fecha o navegador, liberando os recursos.
    driver.quit()

    return property_dict

