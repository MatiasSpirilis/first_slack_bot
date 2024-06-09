import time
import os
import random
import schedule
import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from pytz import timezone

# Path para el archivo env
dotenvpath = os.path.join(os.path.dirname(__file__), 'config.env') 

# Carga las variables de entorno
load_dotenv(dotenvpath) 

# GOOGLE

# Ruta al archivo de credenciales JSON de la cuenta de servicio
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

# Alcances requeridos por la API de Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID de la hoja de cálculo y rango de celdas a leer
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('SHEET_RANGE')

credentials_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Crear las credenciales
creds = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
""" creds = Credentials.from_service_account_file(
    './googlekey/users-test-425300-aad434e40ef6.json', scopes=SCOPES) """

# Conectar con la API de Google Sheets
service = build('sheets', 'v4', credentials=creds)

# GOOGLE > Obtener datos de google sheets

# Llamar a la API para obtener los valores
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGE_NAME).execute()
users_sheets_list = result.get('values', [])

# users_sheets_list = [['Katia', 'Federico', 'Matias', 'Federico', 'Jimena'], ['Federico', 'Matias', 'Federico', 'Matias', 'Federico']]

# users_sheets_list = [['Matias', 'Pablo', 'Matias', 'Pablo', 'Matias'], ['Pablo', 'Matias', 'Pablo', 'Matias', 'Pablo']]

# Variables de entorno
bot_token = os.getenv('BOT_KEY')
channel_id_1 = os.getenv('CHANNEL_ID_1')
channel_id_2 = os.getenv('CHANNEL_ID_2')
channel_id_3 = os.getenv('CHANNEL_ID_3')
mention_users = os.getenv('MENTION_USERS').split(' ')

# Diccionario para mapear los users
users_sheet_ids = {
    'Matias': os.getenv('USER_MATIAS'),
    'Pablo': os.getenv('USER_PABLO'),
    #'Katia': '<@U073PEV83ML>',
    #'Federico': '<@U073FG0EZ7H>'
}

monday_users = [users_sheet_ids.get(users_sheets_list[0][0]),users_sheet_ids.get(users_sheets_list[1][0])]
tuesday_users = [users_sheet_ids.get(users_sheets_list[0][1]),users_sheet_ids.get(users_sheets_list[1][1])]
wednesday_users = [users_sheet_ids.get(users_sheets_list[0][2]),users_sheet_ids.get(users_sheets_list[1][2])]
thursday_users = [users_sheet_ids.get(users_sheets_list[0][3]),users_sheet_ids.get(users_sheets_list[1][3])]
friday_users = [users_sheet_ids.get(users_sheets_list[0][4]),users_sheet_ids.get(users_sheets_list[1][4])]

# Diccionario para mapear dias de la semana a usuarios
users_schedule = {
    0: monday_users,    # Lunes
    1: tuesday_users,   # Martes
    2: wednesday_users, # Mierc
    3: thursday_users,  # Jueves
    4: friday_users,    # Viernes
}

# Iniciar cliente de Slack
client = WebClient(token=bot_token)   

def send_slack_message(channel_id, message):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        print(f"Message sent to {channel_id}: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Error sending message to {channel_id}: {e.response['error']}")

def hydrate():
    print("Executing hydrate function")
    argentina_tz = timezone('America/Argentina/Buenos_Aires')
    now = datetime.now(argentina_tz)
    print(f"Current time: {now}")
    if now.weekday() < 7 and 9 <= now.hour < 23:  # Lunes es 0 y domingo es 6
        messages = [
            "Time to hydrate and move for a bit!!",
            "Don't forget to drink water and stretch!",
            "Take a break, hydrate yourself!",
            "Stay hydrated and take a moment to relax!",
            "Water break! Keep yourself refreshed!"
        ]
        message = random.choice(messages)
        try:
            send_slack_message(channel_id_1, f"{message} {' '.join(mention_users)}")
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

def payroll_monthly():
    argentina_tz = timezone('America/Argentina/Buenos_Aires')
    now = datetime.now(argentina_tz)    
    if now.day == 29:
        try:
            send_slack_message(channel_id_3, f"Remember to send your payroll!")
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")

def inbox():
    # Zona horaria de Arg
    argentina_tz = timezone('America/Argentina/Buenos_Aires')
    now = datetime.now(argentina_tz)
    if now.weekday() < 7:  # Lunes es 0 y domingo es 6
        users_to_mention = users_schedule.get(now.weekday(), ["", ""])
        message = f"{users_to_mention[0]} {users_to_mention[1]} Inbox shift!"
        send_slack_message(channel_id_2, message)


# Programo la tarea para que se ejecute cada 1 hora
# schedule.every().hour.do(hydrate)
# Programo la tarea para que se ejecute cada 1 minuto (testeo)
# schedule.every(1).minutes.do(hydrate)

# Programo la tarea para que se ejecute a las 16:00 de lunes a viernes
schedule.every().monday.at("16:00").do(inbox)
schedule.every().tuesday.at("16:00").do(inbox)
schedule.every().wednesday.at("14:31").do(inbox)
schedule.every().thursday.at("18:32").do(inbox)
schedule.every().friday.at("19:36").do(inbox)

# Programo la tarea para que se ejecute el 29 a las 12:00 de cada mes
schedule.every().day.at("15:00").do(payroll_monthly)


def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(1) # Ejecuta cualquier tarea programada que este pendiente

if __name__ == "__main__":
    main_loop() # Bucle principal

# Para obtener el codigo de autenticacion, nuevamente googlie y encontre estos pasos:
# Crear una aplicacion en la pagina de Slack API: Applications
# Basic Information > Add Features > Incoming webhooks, bots, permissions.
# Scopes: channels:join, channels:read, chat:write.
# Reinstall to workspace.
# Una vez creada, ve a la sección "OAuth & Permissions" y genera un "Bot User OAuth Token"
# Copia y pegar token en la linea 8.
# Para el ID del canal, hacer click derecho en el nombre del canal y seleccionar 'copiar enlace'. El ID del canal en teoria va a ser la parte que venga despues de '/archives/'. Copiar y pegar en la linea 11.
# Buscar como funcionan los entornos virtuales de python para poder deployear el codigo.
# Buscar como conectarme a google sheets para traer los usuarios 