import os
from dotenv import load_dotenv

def load_env_variables():
  load_dotenv()
  env_variables =  {
    'BOT_TOKEN': os.getenv("BOT_TOKEN"),
    'ADMIN_CHANNEL_ID': os.getenv("ADMIN_CHANNEL_ID"),
    'AVAILABILITY_CHANNEL_ID': os.getenv("AVAILABILITY_CHANNEL_ID"),
    'GAME_CHANNEL_ID': os.getenv("GAME_CHANNEL_ID"),
    'FORUM_ID': os.getenv("FORUM_ID"),
    'API_ROUTE': os.getenv("API_ROUTE"),
    'BASE_URL': os.getenv("BASE_URL"),
    'BASE_IMG_URL': os.getenv("BASE_IMG_URL"),
    'TMDB_KEY': os.getenv('TMDB_KEY'),
    'TMDB_BASE_URL': os.getenv('TMDB_BASE_URL'),
  }
  return env_variables

def check_env_variables(env_variables):
  # Check that all environment variables are defined
  for variable_name in env_variables.keys():
    if not env_variables[variable_name]:
      raise Exception(f"{variable_name} is not defined in .env file")