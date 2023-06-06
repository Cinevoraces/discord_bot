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
API_ROUTE = os.getenv("API_ROUTE")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
  if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is not defined in .env file")
  if not CHANNEL_ID:
    raise Exception("CHANNEL_ID is not defined in .env file")
  if not API_ROUTE:
    raise Exception("API_ROUTE is not defined in .env file")
  
  print(f"Logged in as {bot.user.name} ({bot.user.id})")
  print("------")
  channel = bot.get_channel(int(CHANNEL_ID))
  print(f"{bot.user.name} is listenning to {channel.name}")
  await channel.send(f"Hello, {bot.user.name} is ready to go !")

@bot.command()
async def import_last_movie(ctx):
    await ctx.send("Importing movies...")

    response = requests.get(API_ROUTE);
    if response.status_code == 200:
      last_movie = response.json()[0]
      print(type(last_movie))
      print(last_movie.get("french_title"))
    else:
      print("Error while requesting API")

bot.run(BOT_TOKEN) # Run the bot