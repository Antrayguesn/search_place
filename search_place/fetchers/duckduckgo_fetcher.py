from search_place.utils.duckduck_go_search_utils import get_description_from_duckduckgo
from search_place.fetchers.fetcher import Fetcher

from search_place.error.not_found_error import PlaceNotFoundError


class DuckDuckGOFetcher(Fetcher):
    MATCHING_RULES = {
        "latitude": "latitude",
        "longitude": "longitude",
        "name": "name",
        "link": "link",
        "source_url": "source_url",
        "source_name": "source_name",
        "description": "description",
        "image_link": "image_link",
    }

    def search(self, place_name, user_place):
        data_place = get_description_from_duckduckgo(place_name)

        if data_place is None:
            raise PlaceNotFoundError
        return data_place
