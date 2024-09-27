from openpyxl import Workbook
import csv

# Abrir el archivo CSV
with open('MouserSearchDownload.csv', 'r') as file:
    # Crear un objeto CSV Reader
    csv_reader = csv.reader(file)

    # Crear un nuevo libro de Excel
    workbook = Workbook()
    sheet = workbook.active

    # Leer las filas del archivo CSV y escribir en el libro de Excel
    for row in csv_reader:
        sheet.append(row)

    # Guardar el libro de Excel
    workbook.save('formated-data-mouser.xlsx')