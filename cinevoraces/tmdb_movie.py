import requests, random
from .request_utils import set_headers, check_response

def get_movie(env_variables, query):
    """Get a movie from the API"""
    url = f"{env_variables['TMDB_BASE_URL']}/search/movie?query={query}"
    headers = set_headers(env_variables)

    response = requests.get(url=url, headers=headers)
    
    # Check the response is valid or consistent
    if not check_response(response) or len(response.json()['results']) == 0:
        return None, { "message": "Aucun film trouvé."}
    
    return response.json()['results'][0], None

def get_movie_availability(env_variables, tmdb_movie_id, region):
    url = f"{env_variables['TMDB_BASE_URL']}/movie/{tmdb_movie_id}/watch/providers"
    headers = set_headers(env_variables)

    response = requests.get(url=url, headers=headers)
    response.raise_for_status() # Raise an exception if the status code is not 200

    if not check_response(response) or len(response.json()['results']) == 0:
        return None, { "message": "Aucune région de diffusion trouvée pour ce film."}
    
    global_availability = response.json()['results']

    if region not in global_availability :
        return None, { "message": f"Aucun résultat pour la région {region}."}
    
    return global_availability[region], None

def get_random_picture_from_movie(env_variables, tmdb_movie_id):
    url = f"{env_variables['TMDB_BASE_URL']}/movie/{tmdb_movie_id}/images"
    headers = set_headers(env_variables)

    response = requests.get(url=url, headers=headers)
    response.raise_for_status() # Raise an exception if the status code is not 200

    if not check_response(response) or len(response.json()['backdrops']) == 0:
        return None, { "message": "Aucune image trouvée pour ce film."}
    
    image = random.choice(response.json()['backdrops'])
    if not image['file_path']:
        return None, { "message": "Aucune image trouvée pour ce film."}
    
    return image, None