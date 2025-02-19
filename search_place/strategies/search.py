import requests
import hashlib
import base64
import json, simplejson
import time


info_lieu = {}

PROGRESS_BAR = "{} | {}"

CACHE_TIME_DAYS = 5

WIKI_URL = "https://en.wikipedia.org/w/api.php?action=opensearch&search={search}&format=json" 


class SearchError(Exception):
    pass


# Wikipedia
def wikipedia_search(place_name: str):
    res = requests.get(WIKI_URL.format(search=place_name))
    return res.json()


# Google

counter = 0

try:
  with open("search.database", "r") as database:
      info_lieu = json.load(database)
except FileNotFoundError:
    pass

with open("endroit.txt", "r") as fichier:
    for line in fichier:
        data = {}
        print("#"*120)
        counter += 1

        splited_line = line.split(":")
        nom_lieu = splited_line[0].strip()

        print(PROGRESS_BAR.format(counter, nom_lieu))

        # Hashage du nom du lieu pour s'en servir en temps qu'identifiant
        #hash_lieu = hashlib.sha1(nom_lieu.lower().encode()).hexdigest()
        hash_lieu = hashlib.sha1(nom_lieu.encode()).hexdigest()
        if hash_lieu not in info_lieu:
            info_lieu[hash_lieu] = {}
            
        # Récupération de la description utilisateur du lieu
        try:
            description = splited_line[1].replace("\n", "").strip()
            info_lieu[hash_lieu]['user_description'] = description
        except IndexError:
            description = None
            continue

        # Controle du cache
        if "timestamp" in info_lieu[hash_lieu]:
            if time.time() - info_lieu[hash_lieu]["timestamp"] > CACHE_TIME_DAYS * 86400:
                print("Lieu en cache, pas de rechargement")
                continue 
        
        # Recherche DuckDuckGo, première recherche avec le nom du lieu ou le nom sur Internet
        # On evite au plus les appels vers google car payant
        try:
            if "name" in info_lieu[hash_lieu]:
                data = get_description_from_duckduckgo(info_lieu[hash_lieu]["name"], locale=LOCALE_NZ)
            else:
                data = get_description_from_duckduckgo(nom_lieu)
        except SearchError:
            print("Erreur lors de la recherche")
            continue

        # Mise à jour des premières informations
        info_lieu[hash_lieu].update(data)

        #if "latitude" not in info_lieu[hash_lieu] or "longitude" not in info_lieu[hash_lieu]:
        #    data_google = get_description_from_google(nom_lieu)
        #    # On fait la recherche dans la locale du pays pour avoir des résultats plus pertinent
        #    data = get_description_from_duckduckgo(data_google["name"], locale=LOCALE_NZ)
        #    data.update(data_google)

        info_lieu[hash_lieu].update(data)

        if counter % 10 == 0:
            with open("search.database", "w", encoding="utf-8") as database:
                json.dump(info_lieu, database, ensure_ascii=False)

with open("search.database", "w", encoding="utf-8") as database:
    json.dump(info_lieu, database, ensure_ascii=False)

print("#"*120)
print(f"Lieux traitée : {counter}")
print(f"DuckDuckGO : {DDG_COUNT} / Google {GOOGLE_COUNT}")
