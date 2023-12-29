import os
from dotenv import load_dotenv
import discord
import scrappers.scrape_manager as scrape_manager
import sql.db_manager as db_manager

load_dotenv()

DISCORD_CLIENT_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

db_path = os.path.join(os.getcwd(), "sql\database.db")


async def scrape_news():
    ch = await client.fetch_channel(CHANNEL_ID)
    stories = []
    # [(article title, article link), ...]
    stories = scrape_manager.scrape_all()

    # check if stories have already been linked
    # remove all linked story from stories
    # for story in stories:
    #     db_manager.does_article_exist(db_path, story[0], story[1])
    #     del stories[i]

    indexes_to_del = []

    for i in range(len(stories)):
        exists = db_manager.does_article_exist(
            db_path, stories[i][0], stories[i][1])
        if exists:
            indexes_to_del.insert(0, i)

    # remove stories that have already been linked
    for index in indexes_to_del:
        print(index)
        del stories[index]

    for story in stories:
        await ch.send(content=f'{story[0]} {story[1]}')
        db_manager.add_article(db_path, story[0], story[1])


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    db_manager.db_setup(db_path)
    await scrape_news()
    exit()


client.run(DISCORD_CLIENT_TOKEN)
