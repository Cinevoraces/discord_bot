import discord
from discord.ext import commands
from dataclasses import dataclass

from cinevoraces.env_variables import load_env_variables, check_env_variables
from cinevoraces.movie_thread import get_thread_infos
from cinevoraces.movie import get_movie, get_movie_availability, set_message_content

env_variables = load_env_variables()

# Create a bot instance
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
    # Check that all environment variables are defined
    check_env_variables(env_variables)
    
    channel = bot.get_channel(int(env_variables['CHANNEL_ID']))
    print(f"{bot.user.name} is listenning to {channel.name}")
    print("------")
    await channel.send(f"Hello, {bot.user.name} is ready to go !")

# Command to import the last movie from the API and create a new thread in the forum
@bot.command()
async def import_last_movie(ctx):
    await ctx.send("Importing movies...")
    forum = bot.get_channel(int(env_variables['FORUM_ID']))

    # Get the thread infos from the API, then format them for the thread creation
    name, content = get_thread_infos(env_variables, forum)

    # Create the new thread in the forum
    await forum.create_thread(name=name, content=content)

# For a given movie, get the streaming availability in a given region
@bot.command()
async def get_streaming_availability(ctx, query, region="FR"):
    movie, error = get_movie(env_variables, query=query)

    if error:
        await ctx.send(error['message'])

    await ctx.send(f"J'ai trouvé le film {movie['title']} !")

    tmdb_movie_id = movie['id']
    availability, error = get_movie_availability(env_variables, tmdb_movie_id, region)
    
    if error:
        await ctx.send(error['message'])
    
    message_content = set_message_content(movie['title'], region, availability)
    await ctx.send(message_content)

# Guess the movie from a given picture, from Cinévoraces database

@dataclass
class Game:
    is_active: bool = False
    movie_title: str = ""

@bot.command()
async def begin_guess_movie(ctx):
    # Get a random movie from database
    # Extract its name
    # Search for the movie on TMDB
    # Get a random picture from the movie
    pass

@bot.command()
async def my_guess(ctx, movie_title):
    # Check if the movie_title is correct (case insensitive)
    # If it is, stop the game and congratulate the player
    # If it is not, send a message to the player to tell him he is wrong
    pass

# Run the bot
bot.run(env_variables['BOT_TOKEN']) # Run the bot