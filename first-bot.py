import os, datetime
from pytz import timezone
from dotenv import load_dotenv
import discord
from discord.ext import commands
from dataclasses import dataclass

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")
    channel = bot.get_channel(int(CHANNEL_ID))
    print(f"{bot.user.name} is listenning to {channel.name}")
    await channel.send(f"Hello, {bot.user.name} is ready to go !")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name} !")

@bot.command()
async def add(ctx, x, y):
    await ctx.send(f"{x} + {y} = {int(x)+int(y)}")
    
@bot.command()
async def sum(ctx, *arr):
    result = 0
    for number in arr:
        result += int(number)
    
    await ctx.send(f"The sum of {arr} is {result}")

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()

@bot.command()
async def start_session(ctx):
  if session.is_active:
    await ctx.send("Session already started")
  else:
      session.is_active = True
      session.start_time = ctx.message.created_at
      converted_date : datetime = session.start_time.replace(tzinfo=datetime.timezone.utc).astimezone(timezone("Europe/Paris")).strftime("%H:%M:%S")
      await ctx.send("Session started at " + converted_date)


bot.run(BOT_TOKEN)

