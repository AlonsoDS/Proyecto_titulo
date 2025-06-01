import requests
from bs4 import BeautifulSoup


url = "https://www.portalinmobiliario.com/venta/propiedades-usadas/_Desde_0_NoIndex_True"

response = requests.get(url)
response= response.content
soup= BeautifulSoup(response, 'html.parser')

ol = soup.find('ol')
a_tags= soup.find_all('a', class_='ui-search-result__content-wrapper ui-search-link')
for a in a_tags:
    link= a['href']
    tipo= a.find("div", {"class":"ui-search-item__group__element ui-search-item__subtitle-grid"}).text
    nombre= a.find("div", {"class":"ui-search-item__title-label-grid"}).text
    divisa= a.find("span", {"class": "andes-money-amount__currency-symbol"}).text
    monto= a.find("span", {"class": "andes-money-amount__fraction"}).text
    #Aqui hay 3 elementos de lista
    lista_ul=a.find_all('li', {"class":"ui-search-card-attributes__attribute"})
    dormitorios= lista_ul[0].text
    banos= lista_ul[1].text
    area= lista_ul[2].text
    ubicacion= a.find("p", {"class": "ui-search-item__group__element ui-search-item__location-label"}).text
    
    
    
    print(f'Link: {link}\nTipo: {tipo}\nNombre: {nombre}\nDivisa: {divisa}\nMonto: {monto}\nDormitorios: {dormitorios}\nBanos: {banos}\nArea: {area}\nUbicacion: {ubicacion}\n')
    