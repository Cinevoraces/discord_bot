import os, datetime
from pytz import timezone
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
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
    MAX_TIME: int = 60*60 # 1 hours

session = Session()

@tasks.loop(seconds=60, count=2)
async def break_reminder():
    # Mandatory for timecheck to run it twice since it will be stopped right after we start the session if we don't.
    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send(f"**You should take a break !** You've been working for {session.MAX_TIME / 60} minutes !")

def date_converter(date):
    return date.replace(tzinfo=datetime.timezone.utc).astimezone(timezone("Europe/Paris")).strftime("%H:%M:%S")
def human_readable_time(duration):
    return str(datetime.timedelta(minutes=duration))

@bot.command()
async def start_session(ctx):
    if session.is_active:
        await ctx.send("Session already started")
    else:
        session.is_active = True
        break_reminder.start()
        session.start_time = ctx.message.created_at
        await ctx.send("Session started at " + date_converter(session.start_time))

@bot.command()
async def end_session(ctx):
    if not session.is_active:
        await ctx.send("No current session")
    else:
        session.is_active = False
        session.end_time = ctx.message.created_at
        duration = datetime.timedelta(minutes=(session.end_time - session.start_time).seconds/60)
        break_reminder.stop()
        await ctx.send("Session ended at " + date_converter(session.end_time) + " after " + str(duration))

bot.run(BOT_TOKEN)

