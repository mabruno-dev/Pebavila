# Importações necessárias para automação web e manipulação de tempo.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Configuração do WebDriver para o Chrome, automatizando a instalação do driver necessário.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Acessa o site de um imóvel específico na Zap Imóveis.
driver.get("https://www.zapimoveis.com.br/imovel/venda-casa-3-quartos-com-churrasqueira-serra-grande-niteroi-rj-168m2-id-2684897903/?")

# Espera 5 segundos para garantir que a página tenha carregado completamente.
time.sleep(5)

# Busca por todos os elementos 'span' na página, que podem conter informações relevantes.
elements = driver.find_elements(By.TAG_NAME, 'span')

# Exemplo de acesso a um elemento específico e impressão de parte do seu texto.
print(elements[68].text[65:75])
i = 0
price_list = []
j = 0

# Itera pelos elementos 'span' para extrair informações específicas.
for element in elements:
    # Verifica se o elemento contém informações de preço.
    if "R$" in element.text:
        index = element.text.index("R$")
        price = ''.join([caractere for caractere in element.text[index:index+30] if caractere.isdigit()])
        price = float(price)
        price_list.append(price)
    
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
            bumero = 0
            for n in loc:
                if bumero != 0:
                    street += n
                    street += ' '
                bumero = 1
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
    if "bathroom" in element.text:
        try:
            index = i+1
            loc = elements[index].text.split()
            bathroom = int(loc[0])
        except:
            i+=1
            continue

    i+=1

# Compila as informações extraídas em um dicionário.
price_dict = {"bathroom": bathroom, 
"parking_spot": parking_spot, 
"bedroom": bedroom, 
"city": city, 
"neighborhood": neighborhood, 
"public_place": public_place, 
"street": street, 
"realty_type": realty_type, 
"square_footage": meters, 
"property_tax": price_list[0], 
"realty": price_list[1]}

# Imprime o dicionário com as informações do imóvel.
print(price_dict)

# Fecha o navegador, liberando os recursos.
driver.quit()
