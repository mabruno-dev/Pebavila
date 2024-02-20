from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode

# Define uma função para extrair dados de um imóvel


def pegar_dados():
    try:
        # Encontra elementos de texto e listas na página
        elements1 = driver.find_elements(By.TAG_NAME, 'p')
        elements2 = driver.find_elements(By.TAG_NAME, 'li')
        # Realiza tratamento de dados para extrair informações relevantes
        elements1_converted = []
        elements2_converted = []
        for c in elements1:
            if c.text == '':
                pass
            else:
                elements1_converted.append(c.text)

        for c in elements2:
            if c.text == '':
                pass
            else:
                elements2_converted.append(c.text)

        for i, element in enumerate(elements1_converted):
            if 'R$' in element and elements1_converted[i-1] == "Entrar" and len(element) < 50:
                price = float(
                    ''.join([caractere for caractere in element if caractere.isdigit()]))
            elif "quarto" in element and len(element) < 11:
                bedroom = int(
                    ''.join([caractere for caractere in element if caractere.isdigit()]))
            elif "m²" in element and "R$" not in element and len(element) < 8:
                meters = ''.join(
                    [caractere for caractere in element if caractere.isdigit()])
                square_footage = float(meters[0:-1])
            elif "banheiro" in element and len(element) < 13:
                bathroom = int(
                    ''.join([caractere for caractere in element if caractere.isdigit()]))
            elif len(element) > 100:
                realty_description = element
            elif "MOBILIA" in unidecode(element.upper()) and len(element) < 50:
                if element == "Mobiliado":
                    realty_furnished = 1
                else:
                    realty_furnished = 0
            elif ("vaga" in element and len(element) < 9):
                parking_space = int(
                    ''.join([caractere for caractere in element if caractere.isdigit()]))
            else:
                parking_space = 0

        for i, element in enumerate(elements2_converted):
            if "CONDOMINIO" in unidecode(element.upper()):
                condo = float(
                    ''.join([caractere for caractere in element if caractere.isdigit()]))

        city = elements2_converted[2]
        neighborhood = elements2_converted[3]
        street = elements2_converted[4]

        # Cria um dicionário com os dados extraídos
        imovel_dict = {'street': street, 'square_footage': square_footage, 'price': price, 'description': realty_description, 'parking_space': parking_space,
                       'bathrooms': bathroom, 'bedroom': bedroom, 'property_tax': None, 'realty_furnished': realty_furnished, 'condo': condo}

        print(imovel_dict)
        return imovel_dict
    except Exception as E:
        print(E)


# Configuração do WebDriver
# service = Service(ChromeDriverManager().install())
# driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Pass the service object to the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
data_imoveis = []

# Abre o site
driver.get('https://www.quintoandar.com.br/comprar/imovel/niteroi-rj-brasil?referrer=home&profiling=true')
# Aguarda o carregamento da página
time.sleep(5)
elements_button = driver.find_elements(By.CLASS_NAME, 'sc-boq37v-0')


def verify_element():
    #element = driver.find_elements(By.TAG_NAME, 'button')
    element = driver.find_elements(By.CSS_SELECTOR, 'Ver mais')
    if not element:
        return 0
    else:
        element.click()


control = 1
while control != 0:
    control = verify_element()


for i ,element in enumerate(elements_button):
    if 'R$' in element[i-1] == "Apartamento":
        element.click()
        driver.switch_to.window(driver.window_handles[-1])
        data_imoveis.append(pegar_dados())
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

j = 0
for element in elements_button:
    print(f'{element.text}-{i}')
    j += 1


'''
# Loop para clicar em até 11 elementos e extrair dados de imóveis
for i in range(0, 11):
    elements[i].click()
    driver.switch_to.window(driver.window_handles[-1])
    data_imoveis.append(pegar_dados())
    driver.close()
    driver.switch_to.window(driver.window_handles[0])'''




print(data_imoveis)
# Não esqueça de fechar o navegador depois de terminar
driver.quit()