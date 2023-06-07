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
        print("Aucun résultat trouvé pour ce film.")
        return
    
    global_availability = response.json()['results']
    return global_availability[region], None

def set_providers_message(service_type, providers_list):
    """Set the message content for a given service type and providers list"""
    if len(providers_list) == 0:
        return f"Aucun service de {service_type} n'a été trouvé pour ce film."
    else:
        return f"Ce film est disponible en {service_type} sur les plateformes suivantes : {', '.join(providers_list)} \n"

def set_message_content(movie_title, region, availability):
    # Extraction of different providers options and flatten it keeping only names
    flatrate, buy, rent = (availability[k] for k in ("flatrate", "buy", "rent"))
    flatrate_providers_name, buy_providers_name, rent_providers_name = (
        list(map(lambda provider: provider['provider_name'], option)) for option in [flatrate, buy, rent]
    )

    message_header = f"Voici les disponibilités de **{movie_title}** pour la région {region} :\n\n"
    message_flatrate = set_providers_message("sVOD", flatrate_providers_name)
    message_rent = set_providers_message("location", rent_providers_name)
    message_buy = set_providers_message("achat", buy_providers_name)

    return message_header + message_flatrate + message_rent + message_buy