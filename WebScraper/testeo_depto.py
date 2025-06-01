import requests
import csv
import time
import random
from bs4 import BeautifulSoup

with open("user-agents.txt", "r") as f:
    user_agents = f.read().split("\n")

with open("deptos.csv", "r") as f_d:
    urls= f_d.read().split("\n")

for url in urls:
    header = {"User-Agent": user_agents[random.randint(0, len(user_agents)-1)]}
        
    response = requests.get(url, headers= header)
    response= response.content
    soup= BeautifulSoup(response, 'html.parser')

    link= url
    tipo= soup.find("span", {"class":"ui-pdp-subtitle"}).text
    nombre= soup.find("h1", {"class":"ui-pdp-title"}).text

    precios= soup.find_all("span", class_="andes-money-amount__fraction")
    monto_uf= precios[0].text
    monto_clp= precios[1].text

    gastos_comunes = soup.find("p", {"class":"ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-maintenance-fee-ltr"}).text

    lista_ADB=soup.find_all('span', {"class":"ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label"})
    area= lista_ADB[0].text
    dormitorios= lista_ADB[1].text
    banos= lista_ADB[2].text

    ubicacion_container= soup.find("div", {"class":"ui-vip-location"})
    ubicacion= ubicacion_container.find("p", {"class": "ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"}).text
    mapa=soup.find("div", {"class":"ui-vip-location__map"})
    link_ubicacion_maps= mapa.find('img', {'class':'ui-pdp-image'}).get('src')

    caracteristicas_container= soup.find("div", {"class":"ui-pdp-container__row ui-pdp-container__row--attributes"})
    lista_caracteristicas=caracteristicas_container.find_all("span", class_="ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--SEMIBOLD")
    orientacion= lista_caracteristicas[0].text
    piscina= lista_caracteristicas[1].text
    mascotas= lista_caracteristicas[2].text
    antiguedad= lista_caracteristicas[3].text
    bodegas= lista_caracteristicas[4].text
    ascensor= lista_caracteristicas[5].text
    terraza= lista_caracteristicas[6].text
    estacionamiento= lista_caracteristicas[7].text
    piso= lista_caracteristicas[8].text

    #Aqui hay que implementar el append al dataset en csv con pandas
    
    
    time.sleep(random.uniform(1,4))

#print(f'Link: {link}\nTipo: {tipo}\nNombre: {nombre}\nMonto en UF: {monto_uf}\nMonto en CLP: {monto_clp}\nGastos comunes: {gastos_comunes}\nDormitorios: {dormitorios}\nBanos: {banos}\nArea: {area}\n')
#print(f'Ubicacion: {ubicacion}\nLink maps: {link_ubicacion_maps}\nOrientacion: {orientacion}\nPiscina: {piscina}\nMascotas: {mascotas}\nAntiguedad: {antiguedad}\nBodegas: {bodegas}\nAscensor: {ascensor}\n')
#print(f'Terraza: {terraza}\nEstacionamientos: {estacionamiento}\nNumero de piso: {piso}\n')