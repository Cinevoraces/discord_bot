import datetime
import requests

def check_thread_already_exists(forum, french_title):
    # Check if a thread with the same title already exists
    for thread in forum.threads:
      if french_title in thread.name:
        print("Thread already exists")
        raise Exception("Thread already exists")

def get_thread_infos(env_variables, forum):
    response = requests.get(f"{env_variables['API_ROUTE']}/movies?where[is_published]=true&sort=desc&limit=1&select[presentation]=true")
    response.raise_for_status() # Raise an exception if the status code is not 200

    if response.status_code != 200:
      print("Error while requesting API")
      return
    
    last_movie = response.json()[0]
    
    id, season_number, french_title, complete_presentation = (last_movie[k] for k in ("id", "season_number", "french_title", "presentation"))

    # Check if a thread with the same movie already exists
    if check_thread_already_exists(forum, french_title): return

    # Preparing data to inject into both title and opening post
    author_pseudo, presentation = (complete_presentation[k] for k in ("author_pseudo", "presentation"))
    episode_number = datetime.datetime.today().strftime("%W") # Week number
    name = f"S{season_number}E{episode_number} - {french_title}"
    content = f"Film proposé cette semaine par @{author_pseudo}, merci à iel :\n\n" + f"*\"{presentation}\"*\n\nLa fiche du film sur le site de référénce : {env_variables['BASE_URL']}/films/{id}"

    return name, content