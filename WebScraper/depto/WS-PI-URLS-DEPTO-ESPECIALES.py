import requests
import csv
import time
import random
from bs4 import BeautifulSoup


with open("user-agents.txt", "r") as f:
    user_agents = f.read().split("\n")

with open("especiales.txt", "r") as f_e:
    especiales= f_e.read().split("\n")

lista=[]
max_paginas=42
i=0
inicio = time.time()

for url_especial in especiales:
    while i <= max_paginas:
        #https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/puente-alto-metropolitana/_Desde_0_OrderId_PRICE_NoIndex_True
        #https://www.portalinmobiliario.com/venta/casa/propiedades-usadas/colina-metropolitana/_Desde_0_PriceRange_0CLP-450000000CLP_NoIndex_True
        #https://www.portalinmobiliario.com/venta/departamento/propiedades-usadas/rm-metropolitana/nunoa/diagonal-oriente-o-diego-de-almagro/_Desde_0_NoIndex_True

        desde_numero=f"_Desde_{49*i}_"
        url_raw = url_especial
        url = url_raw.replace("_Desde_0_", desde_numero)
        i+=1
        header = {"User-Agent": user_agents[random.randint(0, len(user_agents)-1)]}
        
        response = requests.get(url, headers= header)
        if response.status_code == 200:
            response= response.content
            soup= BeautifulSoup(response, 'html.parser')
            ol = soup.find('ol')
            publicaciones= ol.find_all('li', class_="ui-search-layout__item")
            for p in publicaciones:
                a_tag= p.find('a', class_='poly-component__title')
                link= a_tag['href']
                lista.append(link)
            time.sleep(random.uniform(1,4))
        else:
            i=10000
            print(i)
            print("No quedan mas resultados")
    i=0
        

with open('links_departamentos.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for link in lista:
        writer.writerow([link])
    
fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"El tiempo de ejecución es: {tiempo_ejecucion} segundos")  
print("CSV generado.")