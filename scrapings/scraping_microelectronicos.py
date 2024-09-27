from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook

# Ruta al archivo chromedriver.exe
chrome_driver_path = 'C://Users//santi//OneDrive//Escritorio//Projects//tesis//tesis//chromedriver.exe'

# Configuración del controlador de Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar Chrome en modo headless (sin interfaz gráfica)
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options)


imageurl_Result = []
datasheet_Result = []
prices_Result = []
names_Result = []
url_results = []                                                                                                                                                                                                                                                                                                          
for i in range(10, 1000):
    url = f'http://www.microelectronicos.com/shopexd.asp?id={i}'

    # Cargar la página web con Selenium
    driver.get(url)

    # Encontrar los elementos utilizando XPath
    try:
        xpath_expression_price = '//*[@id="productexdright"]/table/tbody/tr[2]/td[2]/div[1]/span[2]'
        price = driver.find_element(By.XPATH, xpath_expression_price)

        # Obtener el texto del precio
        price_text = price.text

        # Encontrar el nombre del producto
        xpath_expression_name = '//*[@id="User"]/h1'
        name = driver.find_element(By.XPATH, xpath_expression_name)
        name_text = name.text

        datasheet_url = None
        image_url = None

        try:

            # Encontrar la URL de la imagen
            xpath_expression_image = '//*[@id="pimage"]'
            image = driver.find_element(By.XPATH, xpath_expression_image)
            image_url = image.get_attribute('src')

            # Encontrar la URL del datasheet
            xpath_expression_datasheet = '//*[@id="xproductextdesc"]/table/tbody/tr[2]/td/table[1]/tbody/tr[1]/td[3]/span/span/a[2]'
            datasheet = driver.find_element(By.XPATH, xpath_expression_datasheet)
            datasheet_url = datasheet.get_attribute('href')
        except:
            pass

        # Agregar los datos a las listas
        names_Result.append(name_text)
        prices_Result.append(price_text)
        url_results.append(url)
        imageurl_Result.append(image_url)
        datasheet_Result.append(datasheet_url)

        # Imprimir la URL de la imagen
        print(image_url)

    except Exception as e:
        print(f"Error en la URL: {url}")
        print(e)
        continue

# Crear un nuevo libro de trabajo
workbook = Workbook()
sheet = workbook.active

# Encabezados de columna
sheet['A1'] = 'Nombre'
sheet['B1'] = 'Precio'
sheet['C1'] = 'URL'
sheet['D1'] = 'URLImagen'
sheet['E1'] = 'URLDatasheet'

# Escribir los datos en el archivo Excel
for row, (name, price, url, image_url, datasheet_url) in enumerate(zip(names_Result, prices_Result, url_results, imageurl_Result, datasheet_Result ), start=2):
    sheet[f'A{row}'] = name
    sheet[f'B{row}'] = price
    sheet[f'C{row}'] = url
    sheet[f'D{row}'] = image_url
    sheet[f'E{row}'] = datasheet_url

# Guardar el archivo de Excel
workbook.save('microelectronicos_scraping2.xlsx')

# Cerrar el navegador
driver.quit()
