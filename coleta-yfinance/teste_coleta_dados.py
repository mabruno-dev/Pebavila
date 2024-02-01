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
driver.get("https://www.zapimoveis.com.br/lancamento/venda-apartamento-1-quarto-inga-niteroi-rj-101m2-id-2659690255/")
# Aguarda o carregamento da página
time.sleep(5)
# Localiza o elemento pelo título e clica nele
# Localiza o botão "Mensagem" pelo atributo `data-cy` e clica nele

message_button = driver.find_elements(By.TAG_NAME, 'strong')
print(message_button)
message_button.click()


