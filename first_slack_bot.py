import time
import os
import schedule
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from pytz import timezone

# Path para el archivo env
dotenvpath = os.path.join(os.path.dirname(__file__), 'config.env') 

# Carga las variables de entorno
load_dotenv(dotenvpath) 

# Variables de entorno
bot_token = os.getenv('BOT_KEY')
channel_id_1 = os.getenv('CHANNEL_ID_1')
channel_id_2 = os.getenv('CHANNEL_ID_2')
mention_users = os.getenv('MENTION_USERS').split(' ')
time_interval = int(os.getenv('TIME_INTERVAL'))

# Obtener los usuarios para cada día de la semana
monday_users = os.getenv('MONDAY_USERS').split(' ')
tuesday_users = os.getenv('TUESDAY_USERS').split(' ')
wednesday_users = os.getenv('WEDNESDAY_USERS').split(' ')
thursday_users = os.getenv('THURSDAY_USERS').split(' ')
friday_users = os.getenv('FRIDAY_USERS').split(' ')

# Diccionario para mapear días de la semana a usuarios
users_schedule = {
    0: monday_users,    # Lunes
    1: tuesday_users,   # Martes
    2: wednesday_users, # Miércoles
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

def job():
    # Zona horaria de Arg
    argentina_tz = timezone('America/Argentina/Buenos_Aires')
    now = datetime.now(argentina_tz)
    if now.weekday() < 5:  # Lunes es 0 y domingo es 6
        users_to_mention = users_schedule.get(now.weekday(), ["", ""])
        message = f"{users_to_mention[0]} {users_to_mention[1]} Inbox shift!"
        send_slack_message(channel_id_2, message)

# Programar la tarea para que se ejecute a las 16:00 de lunes a viernes
schedule.every().monday.at("16:00").do(job)
schedule.every().tuesday.at("16:00").do(job)
schedule.every().wednesday.at("16:00").do(job)
schedule.every().thursday.at("16:00").do(job)
schedule.every().friday.at("16:00").do(job)

def main_loop():
    while True:
        schedule.run_pending() # Ejecuta cualquier tarea programada que esté pendiente
        try:
            # Envia un mensaje de recordatorio a otro canales 
            send_slack_message(channel_id_1, f"Time to hydrate and move for a bit!! {' '.join(mention_users)}")
            time.sleep(time_interval)
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")
        except KeyboardInterrupt:
            print("Deteniendo el bot...")
            break

if __name__ == "__main__":
    main_loop() # Inicia el bucle principal si el script se ejecuta directamente


# Para obtener el codigo de autenticacion, nuevamente googlie y encontre estos pasos:
# Crear una aplicacion en la pagina de Slack API: Applications
# Basic Information > Add Features > Incoming webhooks, bots, permissions.
# Scopes: channels:join, channels:read, chat:write.
# Reinstall to workspace.
# Una vez creada, ve a la sección "OAuth & Permissions" y genera un "Bot User OAuth Token"
# Copia y pegar token en la linea 8.
# Para el ID del canal, hacer click derecho en el nombre del canal y seleccionar 'copiar enlace'. El ID del canal en teoria va a ser la parte que venga despues de '/archives/'. Copiar y pegar en la linea 11.
# Buscar como funcionan los entornos virtuales de python para poder deployear el codigo.
