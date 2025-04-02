from search_place.utils.nominatim_search_utils import NominatimSearchUtils
from search_place.fetchers.fetcher import Fetcher

from search_place.error.not_found_error import PlaceNotFoundError


class NominatimFetcher(Fetcher):
    MATCHING_RULES = {
        "latitude": "lat",
        "longitude": "lon",
        "name": "name",
        "link": ("extratags", "website"),
        "wikipedia": ("extratags", "wikipedia"),
        "type_place": "type",
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

        if data_place is None:
            raise PlaceNotFoundError
        return data_place
