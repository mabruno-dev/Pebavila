from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from browsermobproxy import Server
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager



gecko_driver_path = '/opt/homebrew/bin/geckodriver'  # Update this path
# Set up the service object with the path to GeckoDriver
service = Service(executable_path=gecko_driver_path)

# Pass the service object to the driver
driver = webdriver.Firefox(service=service)

# Abrir uma página
driver.get("https://www.zapimoveis.com.br/venda/imoveis/rj+niteroi/")
# Localizar a div pelo ID, classe, ou outro seletor
# Exemplo: Encontrar div pelo ID
div = driver.find_element_by_tag_name('div')

# Dentro da div, encontrar o elemento 'a' (link)
link = div.find_element_by_tag_name('a')

# Extrair o atributo 'href' (o link propriamente dito)
url = link.get_attribute('href')

print(url)