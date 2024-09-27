import requests
from openpyxl import Workbook


print("hola")
try:
    base_url = "https://api.mouser.com/"
    api_key = "ba5e65c5-2dc1-48fb-aec3-224e097d79c0"
    endpoint = "SearchByKeyword"

    keywords = [
    "Resistor",
    "Capacitor",
    "Inductor",
    "Diode",
    "Transistor",
    "Integrated Circuit",
    "Microcontroller",
    "Op-Amp",
    "Sensor",
    "Switch",
    "Relay",
    "Fuse",
    "Connector",
    "Potentiometer",
    "Crystal Oscillator",
    "Voltage Regulator",
    "Battery",
    "LED",
    "LCD",
    "Motor",
    "Transformer",
    "Thermistor",
    "Thermocouple",
    "Encoder",
    "Optocoupler",
    "Solenoid",
    "Amplifier",
    "Speaker",
    "Capacitive Touch Sensor",
    "Hall Effect Sensor",
    "RFID Reader",
    "Piezo Buzzer",
    "Gas Sensor",
    "Proximity Sensor",
    "Pressure Sensor",
    "Current Sensor",
    "Voltage Divider",
    "Magnetic Reed Switch",
    "Photoresistor",
    "Varistor"
]  # Lista de palabras clave

    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"] = "nombre"
    sheet["B1"] = "url"
    sheet["C1"] = "referencia"
    sheet["D1"] = "precio"
    sheet["E1"] = "datasheeurl"
    sheet["F1"] = "imageurl"

    row_index = 2  # Índice inicial de fila

    for keyword in keywords:
        url = base_url + endpoint
        headers = {"Content-Type": "application/json"}
        params = {"apiKey": api_key}

        data = {
            "SearchByKeywordRequest": {
                "keyword": keyword,
                "records": 0,
                "startingRecord": 0,
                "searchOptions": "string",
                "searchWithYourSignUpLanguage": "string"
            }
        }

        response = requests.post("https://api.mouser.com/api/v1/search/keyword?apiKey=ba5e65c5-2dc1-48fb-aec3-224e097d79c0", json=data, timeout=5)
        if response.status_code == 200:
            # La solicitud se realizó correctamente
            response_data = response.json()
            products = response_data.get("SearchResults", {}).get("Parts", [])
            search_key_list = ["ProductDetailUrl" , "ManufacturerPartNumber" , "PriceBreaks","DataSheetUrl","ImagePath"]


            for product in products:
                if all(param in product for param in search_key_list):
                    
                    detail_url = product["ProductDetailUrl"]
                    manufacturer_part_number = product["ManufacturerPartNumber"]
                    price_breaks = product["PriceBreaks"]
                    datasheetURL = product["DataSheetUrl"]
                    imageURL = product["ImagePath"]
                    
                    print(datasheetURL, imageURL)              

                    if len(price_breaks) > 0:
                        first_price = price_breaks[0]["Price"]
                    else:
                        first_price = "N/A"

                    sheet[f"A{row_index}"] = keyword
                    sheet[f"B{row_index}"] = detail_url
                    sheet[f"C{row_index}"] = manufacturer_part_number
                    sheet[f"D{row_index}"] = first_price
                    sheet[f"E{row_index}"] = datasheetURL
                    sheet[f"F{row_index}"] = imageURL

                    row_index += 1

    # Guardar el libro de trabajo en un archivo Excel
    workbook.save("resultados.xlsx")

except:
    # Ocurrió un error en la solicitud
    print("Error:", response)
