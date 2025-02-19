from search_place.utils.nominatim_search_utils import NominatimSearchUtils
from search_place.fetchers.fetcher import Fetcher

from search_place.data.place import Place

from search_place.error.not_found_error import PlaceNotFoundError


class NominatimFetcher(Fetcher):
    def fetch(self, user_place):
        if user_place.place:
            place = user_place.place
            nom_place = user_place.place.name
        else:
            nom_place = user_place.name

        data_place = NominatimSearchUtils.nomincatim_search(nom_place, user_place.country)

        if data_place is None:
            raise PlaceNotFoundError

        if user_place.place:
            place.merge(**data_place)
        else:
            place = Place.create_new_place(**data_place)

        return place
