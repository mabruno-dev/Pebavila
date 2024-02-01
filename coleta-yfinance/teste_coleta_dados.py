from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

    # Abre o site
driver.get("https://www.zapimoveis.com.br/venda/imoveis/rj+niteroi/?__ab=seo-texts:control,exp-aa-test:B,preco-metro-quadrado:deslog&transacao=venda&onde=,Rio%20de%20Janeiro,Niter%C3%B3i,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ENiteroi,-22.880707,-43.101353,&pagina=1")

# Aguarda o carregamento da página
time.sleep(5)  # Ajuste este tempo conforme necessário

# Localiza o elemento pelo título e clica nele
# Localiza o botão "Mensagem" pelo atributo `data-cy` e clica nele

message_button = driver.find_elements(By.TAG_NAME, 'a')
print(message_button)
#message_button.click()
time.sleep(20)


