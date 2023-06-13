import discord
from discord.ext import commands

from cinevoraces.env_variables import load_env_variables, check_env_variables
from cinevoraces.movie_thread import get_thread_infos
from cinevoraces.tmdb_movie import get_movie, get_movie_availability
from cinevoraces.providers_message import set_message_content

env_variables = load_env_variables()

# Create a bot instance
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
    # Check that all environment variables are defined
    check_env_variables(env_variables)
    
    channel = bot.get_channel(int(env_variables['AVAILABILITY_CHANNEL_ID']))
    print(f"{bot.user.name} is listenning to {channel.name}")
    print("------")
    await channel.send(f"Bonjour, {bot.user.name} est prêt.\nPour demander la disponibilité d'un film, entrez la commande !get_streaming_availability \"Titre de mon film !\" \"Code de région en deux lettres\"\nLe code de région par défaut (sans précision) est FR. Pour la Belgique précisez BE, pour les suisses précisez CH.")

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

# Run the bot
bot.run(env_variables['BOT_TOKEN']) # Run the bot