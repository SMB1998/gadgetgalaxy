import pandas as pd
import pymysql
import uuid
import requests
import random

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'mysql-48c0510-santiagomunoz318-a346.g.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_kb2phR3iv2qKjSqN5QJ',
    'database': 'db',
    'port': 28745,
}

# Función para autenticarse y obtener el token de acceso
def obtener_token():
    url_login = 'http://127.0.0.1:8000/api/login/'
    payload = {'username': 'smb', 'password': '123456'}
    response = requests.post(url_login, json=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error al iniciar sesión: {response.text}")
        return None

# Función para crear un proveedor utilizando el token de acceso
id_provider = 0
def crear_proveedor(access_token):
    url_proveedores = 'http://127.0.0.1:8000/api/providers/'
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'nombre': 'Mouser', 'url':'https://test-url.com', 'direccion':'cra1a-1-1-1', 'country':'Colombia','city':'cali'}
    response = requests.post(url_proveedores, headers=headers, json=payload)
    if response.status_code == 201:
        print("Proveedor creado exitosamente.", response)
        data = response.json()
        id_provider = data['id'] 
        print("Datos de la respuesta:", data)
        return id_provider
    else:
        print(f"Error al crear proveedor: {response.text}")
        return False
# Crear una conexión a la base de datos
connection = pymysql.connect(**db_config)

# Leer el archivo Excel
df = pd.read_excel('resultados.xlsx')

# Cargar los datos en la base de datos después de la autenticación y creación del proveedor
try:
    access_token = obtener_token()
    if access_token:
        id_proveedor = crear_proveedor(access_token)
        with connection.cursor() as cursor:
            # Crear la tabla si no existe
            cursor.execute("""
    CREATE TABLE IF NOT EXISTS components_components (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        url VARCHAR(200),
        referencia VARCHAR(100),
        precio VARCHAR(50),
        image_url VARCHAR(250),
        datasheet_url VARCHAR(250),
        proveedor_id INT,  -- Cambiado de UUIDField a INT
        FOREIGN KEY (proveedor_id) REFERENCES providers_providers (id)  -- Referenciando la clave primaria de la tabla de proveedores
    )
""")

            # Iterar sobre las filas del DataFrame y agregar cada fila a la base de datos
            random_indices = random.sample(range(len(df)), 500)
            for index in random_indices:
        #for index, row in df.iterrows()  :
                row = df.iloc[index]
                # Verificar si hay valores NaN y manejarlos
                if not pd.isna(row['nombre']) and not pd.isna(row['url']) and not pd.isna(row['referencia']) and not pd.isna(row['precio'])  :
                    # Si el precio no es "N/A", insertar en la base de datos
                    if row['precio'] != "N/A":
                        # Generar un UUID único para el ID
                       
                        
                        datasheet_url = row['datasheeurl'] if not pd.isna(row['datasheeurl']) else "N/A"
                        image_url = row['imageurl'] if not pd.isna(row['imageurl']) else "N/A"
                        search_index_provider  = "Mouser"
                        
                        sql = "INSERT INTO components_components ( nombre, url, referencia, precio, datasheet_url, image_url, proveedor_id, search_index_provider  ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, ( row['nombre'], row['url'], row['referencia'], row['precio'], datasheet_url, image_url, id_proveedor, search_index_provider ))
        connection.commit()
        print("Datos cargados en la base de datos correctamente.")
    else:
        print("No se pudo obtener el token de acceso.")
except Exception as e:
    print(f"Error al cargar los datos en la base de datos: {e}")
finally:
    connection.close()