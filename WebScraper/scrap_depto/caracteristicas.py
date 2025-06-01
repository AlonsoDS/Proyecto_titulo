import requests
import csv
import time
from datetime import datetime
import random
import pandas as pd
from bs4 import BeautifulSoup

with open("user-agents.txt", "r") as f:
    user_agents = f.read().split("\n")

with open("deptos.csv", "r") as f_d:
    urls = f_d.read().split("\n")
random.shuffle(urls)
now = datetime.now()

# Crear un DataFrame vacío para almacenar los datos
df = pd.DataFrame(columns=["caracteristicas"])

for url in urls:
    try:
        header = {"User-Agent": user_agents[random.randint(0, len(user_agents)-1)]}
        response = requests.get(url, headers=header)
        response.encoding = 'utf-8'  # Forzar la codificación UTF-8
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer los datos relevantes
        
        caracteristicas_container = soup.find("tbody", {"class": "andes-table__body"})
        lista_caracteristicas = caracteristicas_container.find_all("div", class_="andes-table__header__container")
        for caracteristica in lista_caracteristicas:
            

            # Crear un DataFrame con los datos del sitio actual
            nueva_fila = pd.DataFrame({
                "caracteristicas": [caracteristica.text], 
            })

            # Concatenar al DataFrame principal
            df = pd.concat([df, nueva_fila], ignore_index=True)
            print(caracteristica.text)
            # Guardar el DataFrame en un archivo CSV
            df.to_csv("caracteristicas.csv", index=False)

    except Exception as e:
        print(f"Error con el link {url}: {str(e)}")

    # Esperar entre 1 y 4 segundos antes de hacer la próxima petición
    time.sleep(random.uniform(1, 4))
