def set_providers_message(service_type, providers_list):
    """Set the message content for a given service type and providers list"""
    if len(providers_list) == 0:
        return f"Aucun service de {service_type} n'a été trouvé pour ce film.\n"
    else:
        return f"{service_type} sur les plateformes suivantes : {', '.join(providers_list)} \n"

def set_message_content(movie_title, region, availability):
    # Extraction of different providers options and flatten it keeping only names
    flatrate, buy, rent = (availability[k] if k in availability else [] for k in ("flatrate", "buy", "rent"))
    flatrate_providers_name, buy_providers_name, rent_providers_name = (
        list(map(lambda provider: provider['provider_name'], option if len(option) != 0 else [])) for option in [flatrate, buy, rent]
    )

    message_header = f"Voici les disponibilités de **{movie_title}** pour la région {region} :\n\n"
    message_flatrate = set_providers_message("sVOD", flatrate_providers_name)
    message_rent = set_providers_message("location", rent_providers_name)
    message_buy = set_providers_message("achat", buy_providers_name)

    return message_header + message_flatrate + message_rent + message_buy