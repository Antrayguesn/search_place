from search_place.fetchers.fetcher import Fetcher
from search_place.data.place import Place


class LocalFetcher(Fetcher):
    def fetch(self, user_place):
        if user_place.place and user_place.place_id is None:
            return Place.find({"name": user_place.name, "country": user_place.country})
