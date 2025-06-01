import csv

def eliminar_duplicados(input_file, output_file):
    # Crear un conjunto para almacenar links únicos
    links_unicos = set()

    # Leer el archivo CSV de entrada
    with open(input_file, 'r', newline='', encoding='utf-8') as file_in:
        reader = csv.reader(file_in)
        for row in reader:
            if row:  # Verifica que la fila no esté vacía
                links_unicos.add(row[0])  # Agrega el link al conjunto (automáticamente elimina duplicados)

    # Escribir los links únicos en el archivo CSV de salida
    with open(output_file, 'w', newline='', encoding='utf-8') as file_out:
        writer = csv.writer(file_out)
        for link in links_unicos:
            writer.writerow([link])

    print(f"Se ha generado el archivo '{output_file}' con links únicos.")

# Ejemplo de uso
input_csv = 'link_casas_limpios.csv'  # Cambia este valor por tu archivo de entrada
output_csv = 'casas.csv'  # Nombre del archivo de salida
eliminar_duplicados(input_csv, output_csv)

input_csv = 'link_deptos_limpios.csv'  # Cambia este valor por tu archivo de entrada
output_csv = 'deptos.csv'  # Nombre del archivo de salida
eliminar_duplicados(input_csv, output_csv)