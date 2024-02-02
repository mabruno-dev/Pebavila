from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC

# Define uma função para extrair dados de um imóvel
def pegar_dados():
    # Encontra elementos de texto e listas na página
    elements1 = driver.find_elements(By.CSS_SELECTOR, 'p')
    elements2 = driver.find_elements(By.CSS_SELECTOR, 'li')
    
    # Realiza tratamento de dados para extrair informações relevantes
    price = float(''.join([caractere for caractere in elements1[3].text if caractere.isdigit()]))
    bedroom = int(''.join([caractere for caractere in elements1[5].text if caractere.isdigit()]))
    meters = ''.join([caractere for caractere in elements1[6].text if caractere.isdigit()])
    square_footage = float(meters[0:-1])
    bathroom = int(''.join([caractere for caractere in elements1[10].text if caractere.isdigit()]))
    realty_description = elements1[18].text
    city = elements2[2].text
    neighborhood = elements2[3].text
    street = elements2[4].text
    number = None
    condo = float(''.join([caractere for caractere in elements2[6].text if caractere.isdigit()]))
    
    if elements1[9].text == '-':
        parking_space = 0
    else:
        parking_space = float(elements1.text)
    
    if elements1[12].text == 'Sem mobília':
        realty_furnished = 0
    elif elements1[12].text == '':
        realty_furnished = None
    else:
        realty_furnished = 1
    
    # Cria um dicionário com os dados extraídos
    imovel_dict = {'street': street, 'square_footage': square_footage, 'price': price, 'description': realty_description, 'parking_space': parking_space, 'bathrooms': bathroom, 'bedroom': bedroom, 'property_tax': None, 'realty_furnished': realty_furnished, 'condo': condo}
    
    print(imovel_dict)
    return imovel_dict

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
data_imoveis = []

# Abre o site
driver.get('https://www.quintoandar.com.br/comprar/imovel/niteroi-rj-brasil?referrer=home&profiling=true')
# Aguarda o carregamento da página
time.sleep(5)
elements = driver.find_elements(By.TAG_NAME, 'h3')

i = 0
for element in elements:
    print(f'{element.text}-{i}')
    i += 1

# Loop para clicar em até 11 elementos e extrair dados de imóveis
for i in range(0, 1):
    elements[i].click()
    data_imoveis.append(pegar_dados)
    driver.back

print(data_imoveis)
# Não esqueça de fechar o navegador depois de terminar
driver.quit()

