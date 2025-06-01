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

#with open("deptos.csv", "r") as f_d:
    #urls = f_d.read().split("\n")

with open("deptos_prueba.csv", "r") as f_d:
    urls = f_d.read().split("\n")
    
random.seed(399)

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



i=0
for url in urls:
    try:
        i+=1
        header = {"User-Agent": user_agents[random.randint(0, len(user_agents)-1)]}
        response = requests.get(url, headers=header)
        if response.status_code==403:
            print("Error 403 a las:",datetime.now())#Tarda al rededo de 1 hora y 5 minutos en levantarse el bloqueo
            print("Link numero:", i)
        response.encoding = 'utf-8'  # Forzar la codificación UTF-8
        
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(random.uniform(1, 4))
        # Extraer los datos relevantes
        link = url
        nombre = soup.find("h1", {"class": "ui-pdp-title"}).text
        
        fecha_consultado = now.date()
        fechas_posibles = soup.find_all("p", class_=[
                "ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle",
                "ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title",
                "ui-pdp-background-color--WHITE ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle"
            ])

        # Filtrar aquellos que contienen el texto "Publicado hace" y extraer el valor
        fecha_publicado = np.nan
        for fecha in fechas_posibles:
            texto = fecha.get_text()
            if "Publicado hace" in texto:
                fecha_publicado = texto
                break 
        
        precio = soup.find("div", {"class":"ui-pdp-price__second-line"})
        divisa = precio.find("span", {"class":"andes-money-amount__currency-symbol"}).text
        monto = precio.find("span", {"class":"andes-money-amount__fraction"}).text
        
        
        referencia_precios = soup.find("div", {"class": "ui-pdp-price-comparison__extra-info-wrapper"})
        # Inicializar ppm2 y ppm2_avg como np.nan en caso de que no se encuentren
        ppm2 = np.nan
        ppm2_avg = np.nan

        # Solo intentamos acceder a los datos si referencia_precios no es None
        if referencia_precios is not None:
            precio_por_m2 = referencia_precios.find_all(
                "p", 
                class_="ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-price-comparison__extra-info-element-value"
            )
            # Verificar si los elementos de precio por m² y precio promedio están presentes
            if len(precio_por_m2) > 0:
                ppm2 = precio_por_m2[0].text
            if len(precio_por_m2) > 1:
                ppm2_avg = precio_por_m2[1].text

        ubicacion_container = soup.find("div", {"class": "ui-vip-location"})
        ubicacion = ubicacion_container.find("p", {"class": "ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title"}).text
        mapa = soup.find("div", {"class": "ui-vip-location__map"})
        link_ubicacion_maps = mapa.find('img', {'class': 'ui-pdp-image'}).get('src')

        # Extraer coordenadas desde el link de Google Maps
        if "center=" in link_ubicacion_maps:
            coordenadas = link_ubicacion_maps.split("center=")[1].split("&")[0]  # Extraer latitud y longitud
        else:
            coordenadas = None  # Si no se encuentra, dejar como None o manejar de otra forma

        dict_car = {"superficie_t": np.nan,
                    "superficie_u": np.nan,
                    "terraza": np.nan,
                    "ambientes": np.nan,
                    "dormitorios": np.nan,
                    "banos": np.nan, 
                    "estacionamiento": np.nan,
                    "bodegas": np.nan,
                    "cantidad_pisos": np.nan,
                    "dep_por_piso": np.nan,
                    "piso": np.nan,
                    "tipo_depto": np.nan,
                    "orientacion": np.nan,
                    "antiguedad": np.nan,
                    "gastos_comunes": np.nan
                    }

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
        lista_tabla_caracteristicas = caracteristicas_container.find_all("tr", class_="andes-table__row ui-vpp-striped-specs__row")
        for elem in lista_tabla_caracteristicas:
            caracteristica = elem.find("div", {"class": "andes-table__header__container"}).text
            valor = elem.find("span", {"class": "andes-table__column--value"}).text
            if caracteristica in mapeo_caracteristicas:
                clave_dict = mapeo_caracteristicas[caracteristica]
                dict_car[clave_dict] = valor


        # Verificar si 'gastos_comunes' ya está definido como None o NaN
        if dict_car["gastos_comunes"] is None or (isinstance(dict_car["gastos_comunes"], float) and np.isnan(dict_car["gastos_comunes"])):
            # Intentar encontrar el elemento en el HTML
            gastos_comunes_element = soup.find("p", {"class": "ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-maintenance-fee-ltr"})
            
            # Si el elemento existe, asignar su texto; si no, asignar np.nan
            if gastos_comunes_element is not None:
                dict_car['gastos_comunes'] = gastos_comunes_element.text
            else:
                dict_car['gastos_comunes'] = np.nan
                
        nueva_fila = pd.DataFrame({
                    "link": [link], 
                    "nombre": [nombre], 
                    "fecha_consultado": [fecha_consultado], 
                    "fecha_publicado": [fecha_publicado],
                    "divisa": [divisa], 
                    "monto": [monto], 
                    "ppm2": [ppm2],
                    "ppm2_avg": [ppm2_avg],
                    "superficie_t": [dict_car["superficie_t"]], 
                    "superficie_u": [dict_car["superficie_u"]],
                    "terraza": [dict_car["terraza"]], 
                    "ambientes": [dict_car["ambientes"]], 
                    "dormitorios": [dict_car["dormitorios"]], 
                    "banos": [dict_car["banos"]], 
                    "ubicacion": [ubicacion], 
                    "estacionamiento": [dict_car["estacionamiento"]], 
                    "bodegas": [dict_car["bodegas"]], 
                    "cantidad_pisos": [dict_car["cantidad_pisos"]], 
                    "dep_por_piso": [dict_car["dep_por_piso"]], 
                    "piso": [dict_car["piso"]], 
                    "tipo_depto": [dict_car["tipo_depto"]], 
                    "orientacion": [dict_car["orientacion"]], 
                    "antiguedad": [dict_car["antiguedad"]], 
                    "gastos_comunes": [dict_car["gastos_comunes"]], 
                    "coordenadas": [coordenadas]
                })

        # Concatenar al DataFrame principal
        df = pd.concat([df, nueva_fila], ignore_index=True)

        # Guardar el DataFrame en un archivo CSV
        df.to_csv("datos_deptos_prueba.csv", index=False)

    except Exception as e:
        print(f"Error con el link {url}: {str(e)}")
        error_links.append(url)

    # Esperar entre 1 y 3 segundos antes de hacer la próxima petición
    time.sleep(random.uniform(1, 3))
cantidad_errores = len(error_links)
with open('links_error_1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for link in error_links:
        writer.writerow([link])

fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"El tiempo de ejecución es: {tiempo_ejecucion} segundos")
print(f"Se registraron {cantidad_errores} en 1000 links.")  
