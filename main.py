import os
import logging
import discord
import scrappers.scrape_manager as scrape_manager
import dotenv
from sql.Db_manager import Db_manager

dotenv.load_dotenv()

DISCORD_CLIENT_TOKEN = os.getenv('DISCORD_CLIENT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
LOG_PATH = os.getenv('LOG_PATH')

logging.basicConfig(filename=LOG_PATH,
                    filemode='a',
                    format='%(asctime)s, %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
db = Db_manager()


async def scrape_news():
    ch = await client.fetch_channel(CHANNEL_ID)
    stories = []
    # [(article title, article link), ...]
    stories = scrape_manager.scrape_all()
    logging.info(f"{len(stories)} articles scraped")

    indexes_to_del = []

    # find stories that have already been linked
    for i in range(len(stories)):
        exists = db.does_article_exist(stories[i][0], stories[i][1])
        if exists:
            indexes_to_del.insert(0, i)
    logging.info(f"{len(indexes_to_del)} articles have already been linked")

    # remove stories that have already been linked
    for index in indexes_to_del:
        del stories[index]

    # link stories
    for story in stories:
        logging.info(f"{story[0]}, {story[1]}")
        await ch.send(content=f'{story[0]} {story[1]}')
        db.add_article(story[0], story[1])
    logging.info(f"{len(stories)} articles linked to discord")


async def shutdown_bot():
    logging.info(f"shutting down bot")
    await client.close()
    exit()


@client.event
async def on_ready():
    logging.info(f"starting bot")
    logging.info(f"logged in as {client.user}")
    await scrape_news()
    await shutdown_bot()


client.run(DISCORD_CLIENT_TOKEN)
