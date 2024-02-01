from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
data_imoveis = []

# Abre o site
driver.get('https://www.quintoandar.com.br/imovel/894374892/comprar/kitnet-1-quarto-centro-niteroi?from_route="search_results"&house_tags=newAd&search_id="66dfca15-6e95-47e4-8444-362a23f89c4c"&search_rank=%7B"sortMode"%3A"relevance"%2C"searchMode"%3A"list"%2C"resultsOrigin"%3A"search"%2C"rank"%3A0%2C"personalization"%3Afalse%7D')
# Aguarda o carregamento da página
time.sleep(5)


elements1 = driver.find_elements(By.CSS_SELECTOR, 'p')
elements2 = driver.find_elements(By.CSS_SELECTOR, 'li')
'''
i = 0
for element in elements1:
    print(f'{element.text}-{i}')
    i+=1

#elements1
print(elements1[3].text)
print(elements1[5].text)
print(elements1[6].text)
print(elements1[9].text)
print(elements1[10].text)
print(elements1[12].text)
print(elements1[18].text)
#elements 2
print(elements2[2].text)
print(elements2[3].text)
print(elements2[4].text)
print(elements2[6].text)
print(elements2[7].text)
'''
#tratamento de dados
price = float(''.join([caractere for caractere in elements1[3].text if caractere.isdigit()]))
bedroom = float(''.join([caractere for caractere in elements1[5].text if caractere.isdigit()]))
meters = ''.join([caractere for caractere in elements1[6].text if caractere.isdigit()])
square_footage = float(meters[0:-1])
bathroom =float(''.join([caractere for caractere in elements1[10].text if caractere.isdigit()]))
realty_description = elements1[18].text
city = elements2[2].text
neighborhood = elements2[3].text
street = elements2[4].text
number = None
condo = float(''.join([caractere for caractere in elements2[6].text if caractere.isdigit()]))
#property_tax = float(''.join([caractere for caractere in elements1[7].text if caractere.isdigit()]))

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

dict = {'street': street , 'square_footage': square_footage , 'price': price, 'description': realty_description, 'parking_space': parking_space , 'bathrooms': bathroom , 'bedroom': bedroom, 'property_tax': None, 'realty_furnished':realty_furnished , 'condo': condo }
print(dict)
# Não esqueça de fechar o navegador depois de terminar
driver.quit()
