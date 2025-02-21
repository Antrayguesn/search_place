from search_place.utils.nominatim_search_utils import NominatimSearchUtils
from search_place.fetchers.fetcher import Fetcher

from search_place.error.not_found_error import PlaceNotFoundError
from search_place.data.country import Country


class NominatimFetcher(Fetcher):
    MATCHING_RULES = {
        "latitude": "lat",
        "longitude": "lon",
        "name": "name",
        "link": ("extratags", "website"),
        "wikipedia": ("extratags", "wikipedia"),
        "type_place": "type",
        "country": "country"
    }
    MATCHING_TYPE_RULES = {
        "wilderness_hut": {
            "drinking_water": ("extratags", "drinking_water"),
            "toilets": ("extratags", "toilets"),
            "capacity": ("extratags", "capacity"),
            "mattress": ("extratags", "mattress"),
            "operator": ("extratags", "operator"),
            "reservation": ("extratags", "reservation"),
            "toilets:disposal": ("extratags", "toilets:disposal"),
            "tracks": ("address", "road")
        },
        "track": {
            "track_type": ("extratags", "tracktype")
        }
    }

    def search(self, place_name, user_place):
        data_place = NominatimSearchUtils.nomincatim_search(place_name, user_place.country)
        cca2 = data_place["address"]["country_code"]
        official_name = Country.find_one({"cca2": cca2.upper()}).name["official"]
        data_place["country"] = official_name

        if data_place is None:
            raise PlaceNotFoundError
        return data_place
