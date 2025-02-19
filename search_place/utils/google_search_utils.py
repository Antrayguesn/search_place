import requests
import hashlib
import base64
import json, simplejson
import time


GOOGLE_HEADERS = {'Content-Type': 'application/json', 'X-Goog-Api-Key': 'AIzaSyDJKb9WVy-bKiMYLx1F-6YOBpsWYe9YZCI', 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.location,places.id'}
GOOGLE_URL = 'https://places.googleapis.com/v1/places:searchText'


def search_place(place_name: str):
    print("Recherche google ...")
    
    research = requests.post(GOOGLE_URL, headers=GOOGLE_HEADERS , json={'textQuery': f"{place_name}, {PAYS}"})
    return research.json()


def get_description_from_google(nom_lieu):
    data = {}
    data_places = search_place(nom_lieu)
    try:
        data_place = data_places["places"][0]
        location  = data_place['location']

        data['address']      = data_place['formattedAddress']
        data['id']           = data_place['id']
        data['latitude']     = location['latitude']
        data['longitude']    = location['longitude']
        data['name']         = data_place['displayName']["text"]
        data['registerName'] = nom_lieu
    except IndexError:
        pass
    except KeyError:
        pass

    return data