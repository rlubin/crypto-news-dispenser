import os
from dotenv import load_dotenv
import discord
import scrappers.scrape_manager as scrape_manager

load_dotenv()

DISCORD_CLIENT_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def scrape_news():
    ch = await client.fetch_channel(CHANNEL_ID)
    stories = []
    stories = scrape_manager.scrape_all() # [(article title, article link), ...]

    for story in stories:
        await ch.send(content=f'{story[0]} {story[1]}')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await scrape_news()
    exit()
    

client.run(DISCORD_CLIENT_TOKEN)