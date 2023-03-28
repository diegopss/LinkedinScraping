import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import random
import time
import pandas as pd

url = "https://www.linkedin.com/jobs/search/?currentJobId=3480686192&f_E=1&f_JT=F&geoId=106057199&keywords=Marketing%20E%20Publicidade&location=Brasil"

#lista de user agents usada para corrigir possiveis bloqueios do linkedin, ocasionados por muitas requisições
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
]
options = Options()
options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

# Cria um objeto do Selenium WebDriver
driver = webdriver.Chrome(options=options)

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
dados = {'URL da vaga no linkedin': '', 'Nome da vaga': '','Nome da empresa contratante': '' , 'URL da empresa contratante': '', 'Modelo de contratação': '', 'Tipo de contratação': '', 'Nível de experiência': '',
         'Número de candidaturas para vaga': '', 'Data da postagem da vaga': '', 'Horário do scraping': '', 'Número de funcionários da empresa': '','Número de seguidores da empresa':'', 'Local sede da empresa': '', 'URL da candidatura': ''}

for conteudo in conteudos:
    urlVaga = conteudo['href']

    driver = webdriver.Chrome(options=options)
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
    modeloContratacao = soup2.find('span', class_="jobs-unified-top-card__workplace-type")


    dados['URL da vaga no linkedin'] = urlVaga
    dados['Nome da vaga'] = nomeVaga.string.strip() if nomeVaga is not None else "Not found"
    dados['Nome da empresa contratante'] = nomeEmpresa.string.strip() if nomeEmpresa is not None else "Not found"
    dados['URL da empresa contratante'] = urlEmpresa.get('href') if urlEmpresa is not None else "Not found"
    dados['Tipo de contratação'] = tipoContratacao[1].string.strip() if len(tipoContratacao) >= 1 else "Not found"
    dados['Nível de experiência'] = nivelExp.string.strip() if nivelExp is not None else "Not found"
    dados['Número de candidaturas para vaga'] = numeroCandidaturas.string.strip() if numeroCandidaturas is not None else "Not found"
    dados['Data da postagem da vaga'] = dataPostagem.string.strip() if dataPostagem is not None else "Not found"
    dados['Horário do scraping'] = horarioScraping
    dados['Modelo de contratação'] = modeloContratacao.string.strip() if modeloContratacao is not None else "Not found"

    print(dados['Modelo de contratação'])

    #acessando o link da empresa
    driver = webdriver.Chrome(options=options)
    driver.get(urlEmpresa.get('href'))
    driver.implicitly_wait(10)
    html3 = driver.page_source
    soup3 = BeautifulSoup(html3, "html.parser")
    time.sleep(2)

    #extraido apenas o local da String
    localSede = soup3.find('h3', class_='top-card-layout__first-subline')
    localSede = localSede.get_text() if localSede is not None else "Not found"
    local = re.sub(r'\d.*', '', localSede).strip()

    dados['Local sede da empresa'] = local

    #extraindo apenas o numero dos funcionarios da string
    numeroFuncionarios = soup3.find('a', class_='face-pile__cta')
    numeroFuncionarios = numeroFuncionarios.get_text() if numeroFuncionarios is not None else "Not found"
    numerosF = re.findall('\d+', numeroFuncionarios)[0] if numeroFuncionarios != "Not found" else "Not found"

    dados['Número de funcionários da empresa'] = numerosF

    #extraindo apenas os numeros de seguidores da string
    numeroSeguidores = soup3.find('h3', class_='top-card-layout__first-subline')
    numeroSeguidores = numeroSeguidores.get_text() if numeroSeguidores is not None else "Not found"
    numerosS = re.findall('\d+', numeroSeguidores)[0] if numeroSeguidores != "Not found" else "Not found"

    dados['Número de seguidores da empresa'] = numerosS

    print(dados['Local sede da empresa'])
    df = pd.DataFrame.from_dict(dados, orient='index').T
    df.to_csv('dados.csv', index=False, mode='a', header=not os.path.isfile('dados.csv'))
