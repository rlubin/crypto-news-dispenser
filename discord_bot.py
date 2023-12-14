import os
from dotenv import load_dotenv
import discord

load_dotenv()

DISCORD_CLIENT_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

print(f'DISCORD_CLIENT_TOKEN {DISCORD_CLIENT_TOKEN}')
print(f'SERVER_ID {SERVER_ID}')
print(f'CHANNEL_ID {CHANNEL_ID}')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(DISCORD_CLIENT_TOKEN)
