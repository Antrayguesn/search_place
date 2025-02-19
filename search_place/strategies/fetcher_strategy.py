from search_place.strategies.strategy import Strategy

from search_place.conf.fetcher_conf import FETCHER

from search_place.fetchers.duckduckgo_fetcher import DuckDuckGOFetcher
from search_place.fetchers.nominatim_fetcher import NominatimFetcher

from search_place.data.user_place import UserPlace
from search_place.data.log import log

from search_place.error.not_found_error import PlaceNotFoundError


class FetcherStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.FETCHER_DICT = {
            DuckDuckGOFetcher.__name__: DuckDuckGOFetcher,
            NominatimFetcher.__name__: NominatimFetcher
        }

    def load_data(self):
        self.data = UserPlace.find({"place_id": None})
        log("DEBUG_0001", f"{len(self.data)} found")

    def write_data(self):
        if self.output_data:
            for place in self.output_data:
                place.save()

    def process(self):
        self.output_data = []
        for userplace in self.data:
            log("DEBUG_0002", f"Processing user_place : {userplace.id}")
            country_place = userplace.country
            type_place = userplace.type_place

            fetcher = None

            try:
                fetcher_country = FETCHER[country_place]
            except KeyError:
                fetcher_names = FETCHER["default"]

            if fetcher is None:
                try:
                    fetcher_names = fetcher_country[type_place]
                except KeyError:
                    fetcher_names = fetcher_country["default"]

            for fetcher_name in fetcher_names:
                fetcher = self.FETCHER_DICT[fetcher_name]()
                try:
                    ret = fetcher.fetch(userplace)
                except PlaceNotFoundError:
                    log("WARNIG_0001", f"Unable to find the place {userplace.name}")
                    continue
                if ret:
                    self.output_data.append(ret)
                    userplace.place_id = ret.id
                    userplace.update()
                    self.output_data.save()
        return [n.to_dict() for n in self.output_data]
