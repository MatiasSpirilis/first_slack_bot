import time
from slack_sdk import WebClient # Importamos WebClient para interactuar con la API de Slack.
from slack_sdk.errors import SlackApiError # Importamos SlackApiError para manejar errores que puedan ocurrir.
# Para instalar la library 'slack_sdk' googlie y habria que hacer esto: abrir una terminal y ejecutar el siguiente comando: pip install slack_sdk


slack_token = ''
# Necesito el token de autenticacion. Pedirle a Jose o hacer mi propio slack para probar.

channel_id = ''
# Channel donde el bot enviara los mensajes (espero je).

client = WebClient(token=slack_token)   


def send_messages(message):
    # function para enviar mensaje a un canal de slack
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        print("Mensaje enviado: ", message)
        # Imprime en la consola que el mensaje se haya enviado correctamente.
    except SlackApiError as e:
        # Aparecera un error del tipo 'SlackApiError' si OK es falso.
        assert e.response["ok"] is False
        assert e.response["error"] 
        print(f"Got an error: {e.response['error']}")
        # Si ocurre un error al enviar el mensaje, lo captura e imprime el error en la consola.

while True:
    # Bucle principal para enviar mensajes cada una hora.
    try:
        send_messages("Time to hydrate and move for a bit!!")
        time.sleep(3600)
        # 1 hora = 3600 segs. Espera esa cantidad de tiempo para volver a enviar otro mensaje.
    except KeyboardInterrupt:
        print("Deteniendo el bot...")
        break



# Para obtener el codigo de autenticacion, nuevamente googlie y encontre estos pasos:
# Crear una aplicacion en la pagina de Slack API: Applications
# Una vez creada, ve a la sección "OAuth & Permissions" y genera un "Bot User OAuth Token"
# Copia y pegar token en la linea 8.

# Para el ID del canal, hacer click derecho en el nombre del canal y seleccionar 'copiar enlace'. El ID del canal en teoria va a ser la parte que venga despues de '/archives/'. Copiar y pegar en la linea 11.