# Importações necessárias para automação web e manipulação de tempo.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

driver = webdriver.Safari()

# Abre uma página da web (exemplo: Google)
driver.get("https://www.zapimoveis.com.br/venda/imoveis/rj+niteroi/")

# Espera 5 segundos para garantir que a página tenha carregado completamente.
time.sleep(5)

# Busca por todos os elementos 'span' na página, que podem conter informações relevantes.
elements = driver.find_elements(By.TAG_NAME, 'span')

elements_2 = driver.find_elements(By.TAG_NAME, 'div')

elements_3 = driver.find_elements(By.CLASS_NAME,"l-card__content")

list_dict = []
# Exemplo de acesso a um elemento específico e impressão de parte do seu texto.
i = 0
price_list = []
j = 0
k = 0
y = 0
for element in elements_3:
    time.sleep(5)
    element.click()
    time.sleep(5)
    for element in elements_2:
    #print(f"{element.text}-->{i}")
        if "No anunciante" in element.text and k != 1:
            index = element.text.index("No anunciante")
            number = ''.join([caractere for caractere in element.text[index:index+30] if caractere.isdigit()])
            number = element.text[index+15] + number
            k += 1
        i += 1
        if "denunciar" in element.text and y != 1:
            index = element.text.index("denunciar")
            index2 = element.text.index("Vendas")

            imobiliaria = element.text[index+18:index2] ## ver se vai precisar ajustar tamanho para outras imobiliarias##
            y += 1

        if "Características" in element.text:
            index = element.text.index("Características")
            index2 = element.text.index("Mostrar mais")
            descricao = element.text[index:index2]
        

    i = 0
    # Itera pelos elementos 'span' para extrair informações específicas.
    for element in elements:
        # Verifica se o elemento contém informações de preço.
        #print(f"{element.text}-->{i}")
        try:
            if "R$" in element.text:
                index = element.text.index("R$")
                price = ''.join([caractere for caractere in element.text[index:index+30] if caractere.isdigit()])
                price = float(price)
                price_list.append(price)
        except:
            price_list.append('None')
        
        # Verifica se o elemento contém informações de metragem quadrada.
        if "m²" in element.text:
            if j == 0:
                meters = ''.join([caractere for caractere in element.text if caractere.isdigit()])
                meters = float(meters[0:-1])
            j += 1

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
        if "bedroom" in element.text:
            try:
                index = i+1
                loc = elements[index].text.split()
                bedroom = int(loc[0])
            except:
                i+=1
                continue
        if "parking" in element.text:
            try:
                index = i+1
                loc = elements[index].text.split()
                parking_spot = int(loc[0])
            except:
                i+=1
                continue
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

        if "Na planta" in element.text:
            lancamento = 0
        elif "Em construcao" in element.text:
            lancamento = 1
        else:
            lancamento = 2
        


        i+=1
    # Compila as informações extraídas em um dicionário.
    price_dict = {
        "city": city, 
        "neighborhood": neighborhood, 
        "street": street, 
        "realty_type": realty_type,
        "realty_number": number,
        "square_footage": meters, 
        "property_tax": price_list[0], 
        "price": price_list[1],
        "rent_price": price_list[0], ##ainda nao implementado##
        "description": descricao,
        "parking_spot": parking_spot, 
        "bathroom": bathroom, 
        "bedroom": bedroom, 
        "real_state_office": imobiliaria,
        "realty_number": number,
        "done": lancamento
        #"public_place": public_place,
        #"state": state_name,           
                }

    list_dict.append(price_dict)
    time.sleep(5)

# Fecha o navegador, liberando os recursos.
driver.quit()
