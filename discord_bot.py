import os
from dotenv import load_dotenv
import discord
import asyncio
import scrape_manager

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
    ch = await client.fetch_channel(CHANNEL_ID)

    stories = scrape_manager.scrape_all() # [(article title, article link), ...]

    for story in stories:
        await ch.send(content=f'{story[0]} {story[1]}')

client.run(DISCORD_CLIENT_TOKEN)