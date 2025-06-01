import csv

def truncar_links(input_file, output_file):
    # Leer los links desde el archivo original
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        links_truncados = []

        # Procesar cada link
        for row in reader:
            link = row[0]
            # Truncar el link en la posición 49
            link_truncado = link[:45]
            # Guardar el link truncado
            links_truncados.append(link_truncado)
    
    # Escribir los links truncados en un nuevo archivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for link in links_truncados:
            writer.writerow([link])

# Truncar links de casas
truncar_links('links_casas.csv', 'link_casas_limpios.csv')

# Truncar links de departamentos
#truncar_links('links_departamentos.csv', 'link_deptos_limpios.csv')

print("Links truncados guardados en archivos CSV.")
