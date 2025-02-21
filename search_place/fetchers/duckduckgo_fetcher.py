from search_place.utils.duckduck_go_search_utils import get_description_from_duckduckgo
from search_place.fetchers.fetcher import Fetcher

from search_place.data.place import Place


class DuckDuckGOFetcher(Fetcher):
    def fetch(self, user_place):
        if user_place.place:
            place = user_place.place
            nom_place = user_place.place.name
        else:
            nom_place = user_place.name

        data_place = get_description_from_duckduckgo(nom_place)

        if user_place.place:
            new_place = Place(**data_place)
            new_place.type_place = user_place.place.type_place
            place = user_place.place.merge(new_place)
        else:
            place = Place.create(**data_place)

        return place
