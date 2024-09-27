import pandas as pd
import pymysql
import uuid

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'database-1.ctqy4uogoc5y.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': '1c2a7086d0C',
    'database': 'db',
    'port': 3306,
}

# Crear una conexión a la base de datos
connection = pymysql.connect(**db_config)

# Leer el archivo Excel
df = pd.read_excel('microelectronicos_scraping2.xlsx')

# Cargar los datos en la base de datos
try:
    with connection.cursor() as cursor:
        # Iterar sobre las filas del DataFrame y agregar cada fila a la base de datos
        for index, row in df.iterrows():

            # Insertar en la base de datos
            datasheet_url = row["URLDatasheet"] if not pd.isna(row["URLDatasheet"]) else "N/A"
            image_url = row["URLImagen"] if not pd.isna(row["URLImagen"]) else "N/A"
            sql = "INSERT INTO components_components ( nombre, url, precio, proveedor_id, image_url, datasheet_url) VALUES ( %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ( row['Nombre'], row['URL'], row['Precio'], 2, image_url, datasheet_url ))
    connection.commit()
    print("Datos cargados en la base de datos correctamente.")
except Exception as e:
    print(f"Error al cargar los datos en la base de datos: {e}")

# Cerrar la conexión a la base de datos
connection.close()
