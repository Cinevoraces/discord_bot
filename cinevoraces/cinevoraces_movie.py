import requests
from .request_utils import set_headers, check_response

def get_random_movie_title(env_variables):
    """Get a random movie from Cinévoraces API"""
    url = f"{env_variables['API_ROUTE']}/movies/random-posters/2"

    response = requests.get(url=url)

    response.raise_for_status() # Raise an exception if the status code is not 200
    if not check_response(response) or len(response.json()) == 0:
        print("Aucun film trouvé.")
        return

    if response.status_code != 200:
        print("Error while requesting API")
        return None, { "message": "Erreur lors de la requête à l'API."}
    
    return response.json()[0]['french_title'], None