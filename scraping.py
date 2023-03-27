import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

url = "https://www.linkedin.com/jobs/search/?currentJobId=3480686192&f_E=1&f_JT=F&geoId=106057199&keywords=Marketing%20E%20Publicidade&location=Brasil"

# Cria um objeto do Selenium WebDriver
driver = webdriver.Chrome()

# Navega para a página desejada
driver.get(url)

# Espera até que todos os elementos sejam carregados (pode ser necessário ajustar o tempo de espera)
driver.implicitly_wait(10)

time.sleep(3)

# Simula a rolagem da página até o final
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera um pouco para a página carregar novamente
time.sleep(3)
# Simula a rolagem da página até o final
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera um pouco para a página carregar novamente
time.sleep(3)
# Simula a rolagem da página até o final
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera um pouco para a página carregar novamente
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Espera um pouco para a página carregar novamente
time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Extrai o HTML da página carregada
html = driver.page_source

# Cria um objeto BeautifulSoup a partir do HTML
soup = BeautifulSoup(html, "html.parser")

conteudos = soup.find_all('a', href= re.compile('/jobs/view'))
urlVagas = []
tam = 0
for conteudo in conteudos:
    urlVagas.append(conteudo)

#for vaga in soup.find_all('a', href=True):
 #   if '/jobs/view' in vaga['href']:
  #      urlVagas.append(vaga['href'])

for vaga in urlVagas:
    print(vaga['href'])

print(len(urlVagas))

print(len(urlVagas))