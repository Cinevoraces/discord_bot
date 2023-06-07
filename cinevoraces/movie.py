import requests
# from request_utils import set_headers, check_response
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
        print("Aucun résultat trouvé.")
        return
    
    return response.json()['results'], None