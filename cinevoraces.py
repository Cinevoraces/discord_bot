import discord
from discord.ext import commands
from dataclasses import dataclass

from cinevoraces.env_variables import load_env_variables, check_env_variables
from cinevoraces.movie_thread import get_thread_infos
from cinevoraces.tmdb_movie import get_movie, get_movie_availability, get_random_picture_from_movie
from cinevoraces.providers_message import set_message_content
from cinevoraces.cinevoraces_movie import get_random_movie_title

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
    # Get a random movie from cinévoraces database
    random_cinevoraces_movie_title, error = get_random_movie_title(env_variables)
    if error:
        await ctx.send(error['message'])
    print(random_cinevoraces_movie_title)
    # Search for the movie on TMDB and get its id
    tmdb_movie, error = get_movie(env_variables, query=random_cinevoraces_movie_title)
    if error:
        await ctx.send(error['message'])
    tmdb_movie_id = tmdb_movie['id']
    print(tmdb_movie_id)
    # Get a random picture from the movie
    image, error = get_random_picture_from_movie(env_variables, tmdb_movie_id)
    if error:
        await ctx.send(error['message'])
    
    image_url = f"https://www.themoviedb.org/t/p/original{image['file_path']}"
    await ctx.send(f"Devinez le film à partir de cette image !\n\n{image_url}")

@bot.command()
async def my_guess(ctx, movie_title):
    # Check if the movie_title is correct (case insensitive)
    # If it is, stop the game and congratulate the player
    # If it is not, send a message to the player to tell him he is wrong
    pass

# Run the bot
bot.run(env_variables['BOT_TOKEN']) # Run the bot