import requests
import simplejson

from search_place.error.search_error import SearchError
from search_place.error.not_found_error import PlaceNotFoundError

DUCKDUCK_URL = "https://duckduckgo.com/?q={search}&kl={locale}&format=json&kp=-2&kc=1&kaf=1"
PAYS = "New Zealand"
LOCALE = "fr-fr"
LOCALE_NZ = "nz-en"
IMAGE_URL = "https://duckduckgo.com/{image}"


# DuckDuckGO
def duckduckgo_search(place_name: str, locale=LOCALE):
    res = requests.get(DUCKDUCK_URL.format(search=place_name, locale=locale))

    if res.status_code >= 300:
        raise SearchError

    try:
        return res.json()
    except simplejson.errors.JSONDecodeError:
        return None


def get_description_from_duckduckgo(nom_lieu: str, locale=LOCALE_NZ):
    data = {}

    data_activities = duckduckgo_search(nom_lieu, locale=locale)

    if data_activities is None or data_activities["Heading"] == '':
        raise PlaceNotFoundError(f"Unable to found the place {nom_lieu}")

    if "Infobox" in data_activities and data_activities["Infobox"]:
        try:
            coordinates = next(item for item in data_activities["Infobox"]["content"] if item["label"] == "Coordinates")["value"]
            data['latitude'] = coordinates["latitude"]
            data['longitude'] = coordinates["longitude"]
        except KeyError:
            pass
        except StopIteration:
            pass

    try:
        data["name"] = data_activities["Heading"]
    except KeyError:
        pass

    if data_activities["AbstractText"]:
        data['description'] = f"{data_activities["AbstractText"]}"
        data['source_url'] = data_activities["AbstractURL"]
        data['source_name'] = data_activities["AbstractSource"]

    if data_activities["Results"]:
        try:
            data['link'] = data_activities["Results"][0]["FirstURL"]
        except IndexError:
            pass
    if data_activities["Image"]:
        data['image_link'] = "{{" + IMAGE_URL.format(image=data_activities["Image"]) + f"|{data_activities["ImageWidth"]}" + "}}"

    return data
