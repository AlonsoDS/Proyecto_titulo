import sys
import traceback
import requests
import csv
import time
from datetime import datetime
import random
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

with open("user-agents.txt", "r") as f:
    user_agents = f.read().split("\n")

with open("deptos.csv", "r") as f_d:
    urls = f_d.read().split("\n")

#with open("deptos_prueba.csv", "r") as f_d:
    #urls = f_d.read().split("\n")
    
random.seed(16)

error_links = []

inicio = time.time()

now = datetime.now()

# Crear un DataFrame vacío para almacenar los datos
df = pd.DataFrame(columns=["link", "nombre", "fecha_consultado", "fecha_publicado", "divisa", "monto",
                           "ppm2", "ppm2_avg", "superficie_t", "superficie_u",
                           "terraza", "ambientes", "dormitorios", "banos", "ubicacion", 
                           "estacionamiento", "bodegas", "cantidad_pisos", "dep_por_piso",
                           "piso", "tipo_depto","orientacion","antiguedad","gastos_comunes",
                           "coordenadas"])

df_error = pd.DataFrame(columns=["link"])

def scrape_property_data(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    link = url
    nombre = soup.find("h1", {"class": "ui-pdp-title"}).text
    fecha_consultado = now.date()
    
    fechas_posibles = soup.find_all("p", class_=[
        "ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle",
        "ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title",
        "ui-pdp-background-color--WHITE ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle"
    ])
    fecha_publicado = np.nan
    for fecha in fechas_posibles:
        if "Publicado hace" in fecha.get_text():
            fecha_publicado = fecha.get_text()
            break
    
    precio = soup.find("div", {"class":"ui-pdp-price__second-line"})
    divisa = precio.find("span", {"class":"andes-money-amount__currency-symbol"}).text
    monto = precio.find("span", {"class":"andes-money-amount__fraction"}).text
    
    referencia_precios = soup.find("div", {"class": "ui-pdp-price-comparison__extra-info-wrapper"})
    ppm2, ppm2_avg = np.nan, np.nan
    if referencia_precios:
        precios = referencia_precios.find_all("p", class_="ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-price-comparison__extra-info-element-value")
        ppm2 = precios[0].text if len(precios) > 0 else np.nan
        ppm2_avg = precios[1].text if len(precios) > 1 else np.nan
    
    
    ubicacion_containers = soup.find_all("p", {"class": "ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"})
    ubicacion = ubicacion_containers[-1].text
    mapa = soup.find("div", {"class": "ui-vip-location__map"})
    coordenadas = mapa.find('img', {'class': 'ui-pdp-image'}).get('src').split("center=")[1].split("&")[0] if mapa else np.nan
    
    dict_car = {key: np.nan for key in ["superficie_t", "superficie_u", "terraza", "ambientes", "dormitorios", "banos", "estacionamiento", "bodegas", "cantidad_pisos", "dep_por_piso", "piso", "tipo_depto", "orientacion", "antiguedad", "gastos_comunes"]}
    
    mapeo_caracteristicas = {
        "Superficie total": "superficie_t",
        "Superficie útil": "superficie_u",
        "Superficie de terraza": "terraza",
        "Ambientes": "ambientes",
        "Dormitorios": "dormitorios",
        "Baños": "banos",
        "Estacionamientos": "estacionamiento",
        "Bodegas": "bodegas",
        "Cantidad de pisos": "cantidad_pisos",
        "Departamentos por piso": "dep_por_piso",
        "Número de piso de la unidad": "piso",
        "Tipo de departamento": "tipo_depto",
        "Orientación": "orientacion",
        "Antigüedad": "antiguedad",
        "Gastos comunes": "gastos_comunes"
    }
    
    caracteristicas_container = soup.find("tbody", {"class": "andes-table__body"})
    if caracteristicas_container:
        for elem in caracteristicas_container.find_all("tr", class_="andes-table__row"):
            caracteristica_elem = elem.find("div", class_="andes-table__header__container")
            valor_elem = elem.find("span", class_="andes-table__column--value")

            if caracteristica_elem and valor_elem:
                caracteristica = caracteristica_elem.text.strip()
                valor = valor_elem.text.strip()

                if caracteristica in mapeo_caracteristicas:
                    dict_car[mapeo_caracteristicas[caracteristica]] = valor
    #print(dict_car)
    nueva_fila = pd.DataFrame([{**dict_car, "link": link, "nombre": nombre, "fecha_consultado": fecha_consultado, "fecha_publicado": fecha_publicado, "divisa": divisa, "monto": monto, "ppm2": ppm2, "ppm2_avg": ppm2_avg, "ubicacion": ubicacion, "coordenadas": coordenadas}])
    return nueva_fila

i = 0
for url in urls:
    try:
        i += 1
        header = {"User-Agent": random.choice(user_agents)}
        response = requests.get(url, headers=header, timeout=10)
        time.sleep(random.uniform(1, 3))  # Ajustar la posición según sea necesario

        if response.status_code == 403:
            print(f"Error 403 at {datetime.now()} - Link #{i}. Saving progress and exiting.")
            df.to_csv("datos_deptos_prueba.csv", index=False)  # Guardar el progreso antes de salir
            with open("last_processed_url.txt", "w") as f:
                f.write(url)  # Guardar el último link con error
            sys.exit()  # Terminar ejecución inmediatamente
        
        elif response.status_code != 200:
            print(f"Error {response.status_code} at {datetime.now()} - Link #{i}")
            continue
        
        response.encoding = 'utf-8'
        
        data_row = scrape_property_data(url, response.text)
        if pd.isna(data_row["coordenadas"].iloc[0]) or pd.isna(data_row["superficie_t"].iloc[0]):
            with open("links_error.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([url])
        else:
            df = pd.concat([df, data_row], ignore_index=True)
            df.to_csv("datos_deptos_prueba.csv", index=False)
        
    except Exception as e:
        tb_list = traceback.extract_tb(sys.exc_info()[2])
        line = tb_list[-1][1]
        print(f"Error with {url}: {str(e)}. Line {line}")
        error_links.append(url)

fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"El tiempo de ejecución es: {tiempo_ejecucion} segundos")
