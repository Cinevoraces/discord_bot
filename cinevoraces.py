import os, datetime, json
from pytz import timezone
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import requests


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
FORUM_ID = os.getenv("FORUM_ID")
API_ROUTE = os.getenv("API_ROUTE")
BASE_URL = os.getenv("BASE_URL")
BASE_IMG_URL = os.getenv("BASE_IMG_URL")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
  if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is not defined in .env file")
  if not CHANNEL_ID:
    raise Exception("CHANNEL_ID is not defined in .env file")
  if not FORUM_ID:
    raise Exception("FORUM_ID is not defined in .env file")
  if not API_ROUTE:
    raise Exception("API_ROUTE is not defined in .env file")
  if not BASE_URL:
    raise Exception("BASE_URL is not defined in .env file")
  if not BASE_IMG_URL:
    raise Exception("BASE_IMG_URL is not defined in .env file")
  
  print(f"Logged in as {bot.user.name} ({bot.user.id})")
  print("------")
  channel = bot.get_channel(int(CHANNEL_ID))
  print(f"{bot.user.name} is listenning to {channel.name}")
  await channel.send(f"Hello, {bot.user.name} is ready to go !")

@bot.command()
async def import_last_movie(ctx):
    await ctx.send("Importing movies...")
    forum = bot.get_channel(int(FORUM_ID))

    response = requests.get(API_ROUTE)

    if response.status_code != 200:
      print("Error while requesting API")
      return
    
    last_movie = response.json()[0]
    
    id, season_number, french_title, complete_presentation = (last_movie[k] for k in ("id", "season_number", "french_title", "presentation"))
    author_pseudo, presentation = (complete_presentation[k] for k in ("author_pseudo", "presentation"))

    print(id, french_title, author_pseudo, presentation)

    episode_number = datetime.datetime.today().strftime("%W") # Week number

    name = f"S{season_number}E{episode_number} - {french_title}"
    content = f"> {presentation}\n\nPar @{author_pseudo}, merci à iel.\n\nLa fiche du film sur le site de référénce : {BASE_URL}/films/{id}"

    await forum.create_thread(name=name, content=content)      

bot.run(BOT_TOKEN) # Run the bot