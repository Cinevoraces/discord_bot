def set_headers(env_variables):
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {env_variables['TMDB_KEY']}",
    }

def check_response(response):
    response.raise_for_status() # Raise an exception if the status code is not 200
    
    if response.status_code != 200:
        print("An error occured")
        return False
    
    return True