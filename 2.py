import discord
import requests
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén las variables de entorno
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Inicializa el cliente de Discord
intents = discord.Intents.default()
intents.message_content = True  # Habilita el acceso al contenido de los mensajes
client = discord.Client(intents=intents)

# ID del canal o servidor específico que quieres monitorear
ID_DEL_CANAL = 1325277401575587984  # Reemplaza con el ID del canal
ID_DEL_SERVIDOR = 1325277401059426356  # Reemplaza con el ID del servidor

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    # Ignora los mensajes enviados por el propio bot
    if message.author == client.user:
        return

    # Verifica si el mensaje es en el canal o servidor específico
    if message.channel.id == ID_DEL_CANAL or message.guild.id == ID_DEL_SERVIDOR:
        # Prepara el mensaje para Telegram
        mensaje_telegram = f"Nuevo mensaje en {message.guild.name}:\nDe: {message.author}\nMensaje: {message.content}"

        # Envía el mensaje a Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje_telegram
        }
        try:
            response = requests.post(url, data=params)
            if response.status_code == 200:
                print("Notificación enviada a Telegram.")
            else:
                print(f"Error al enviar la notificación: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error al conectar con Telegram: {e}")

# Inicia el bot
client.run(DISCORD_TOKEN)