import requests

def search_place(query, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_place_details(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,formatted_phone_number&key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()