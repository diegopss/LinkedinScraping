import os
from datetime import datetime

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
for i in range(1):
    # Simula a rolagem da página até o final
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


# Extrai o HTML da página carregada
html = driver.page_source

# Cria um objeto BeautifulSoup a partir do HTML
soup = BeautifulSoup(html, "html.parser")

conteudos = soup.find_all('a', href= re.compile('/jobs/view'))
dados = {'urlVaga': '', 'nomeVaga': '','nomeEmpresa': '' , 'urlEmpresa': '', 'modeloContratacao': '', 'tipoContratacao': '', 'nivelExp': '',
         'numeroCandidaturas': '', 'dataPostagem': '', 'horarioScraping': '', 'numeroFuncionarios': '', 'localSede': '', 'urlCandidatura': ''}

for conteudo in conteudos:
    urlVaga = conteudo['href']

    driver.get(urlVaga)
    driver.implicitly_wait(10)
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, "html.parser")
    time.sleep(2)

    horarioScraping = datetime.now()
    horarioScraping = horarioScraping.strftime("%d-%m-%Y %H:%M:%S")
    urlVaga = conteudo['href']
    nomeVaga = soup2.find('h1', class_="top-card-layout__title")
    nomeEmpresa = soup2.find('a', class_="topcard__org-name-link")
    urlEmpresa = soup2.find('a', class_="topcard__org-name-link")
    tipoContratacao = soup2.find_all('span', class_= "description__job-criteria-text")
    nivelExp = soup2.find('span', class_= "description__job-criteria-text")
    numeroCandidaturas = soup2.find('span', class_= "num-applicants__caption")
    dataPostagem = soup2.find('span', class_= "posted-time-ago__text")
    #numeroFuncionarios =

    dados['urlVaga'] = urlVaga
    dados['nomeVaga'] = nomeVaga.string.strip() if nomeVaga is not None else "Not found"
    dados['nomeEmpresa'] = nomeEmpresa.string.strip() if nomeEmpresa is not None else "Not found"
    dados['urlEmpresa'] = urlEmpresa.get('href') if urlEmpresa is not None else "Not found"
    dados['tipoContratacao'] = tipoContratacao[1].string.strip() if len(tipoContratacao) >= 1 else "Not found"
    dados['nivelExp'] = nivelExp.string.strip() if nivelExp is not None else "Not found"
    dados['numeroCandidaturas'] = numeroCandidaturas.string.strip() if numeroCandidaturas is not None else "Not found"
    dados['dataPostagem'] = dataPostagem.string.strip() if dataPostagem is not None else "Not found"
    dados['horarioScraping'] = horarioScraping
    #dados['numeroFuncionarios'] =
    print(dados['horarioScraping'])
    df = pd.DataFrame.from_dict(dados, orient='index').T
    df.to_csv('dados.csv', index=False, mode='a', header=not os.path.isfile('dados.csv'))


