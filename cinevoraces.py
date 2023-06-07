import discord
from discord.ext import commands

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

# Run the bot
bot.run(env_variables['BOT_TOKEN']) # Run the bot