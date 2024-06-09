import os
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Path para el archivo env
dotenvpath = os.path.join(os.path.dirname(__file__), 'config.env') 

# Carga las variables de entorno
load_dotenv(dotenvpath) 


# Ruta al archivo de credenciales JSON de la cuenta de servicio
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# Alcances requeridos por la API de Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Crear las credenciales
creds = Credentials.from_service_account_file(
    './googlekey/users-test-425300-aad434e40ef6.json', scopes=SCOPES)

# ID de la hoja de cálculo y rango de celdas a leer
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('SHEET_RANGE')  # Ejemplo de rango

# Conectar con la API de Google Sheets
service = build('sheets', 'v4', credentials=creds)

# Llamar a la API para obtener los valores
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    print(values[0][1])