from search_place.strategies.strategy import Strategy

from search_place.conf.fetcher_conf import FETCHER

from search_place.fetchers.duckduckgo_fetcher import DuckDuckGOFetcher
from search_place.fetchers.nominatim_fetcher import NominatimFetcher
from search_place.fetchers.local_fetcher import LocalFetcher
from search_place.fetchers.DOCHut_fetcher import DOCHutFetcher
from search_place.fetchers.DOCTrack_fetcher import DOCTrackFetcher

from search_place.data.user_place import UserPlace
from search_place.data.place import Place
from search_place.data.log import log

from search_place.error.not_found_error import PlaceNotFoundError

from collections import deque


class FetcherStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.FETCHER_DICT = {
            DuckDuckGOFetcher.__name__: DuckDuckGOFetcher,
            NominatimFetcher.__name__: NominatimFetcher,
            LocalFetcher.__name__: LocalFetcher,
            DOCHutFetcher.__name__: DOCHutFetcher,
            DOCTrackFetcher.__name__: DOCTrackFetcher
        }

    def load_data(self):
        self.data = UserPlace.find({"place_id": None})
        log("DEBUG_0001", f"{len(self.data)} found")

    def write_data(self):
        if self.output_data:
            for place in self.output_data:
                if place:
                    place.save()

    def process(self):
        self.output_data = []
        fetcher_names = deque(FETCHER["default"])
        for userplace in self.data:
            fetcher_country = None
            log("DEBUG_0002", f"Processing user_place : {userplace.id}")
            country_place = userplace.country
            type_place = userplace.type_place

            fetcher = None

            try:
                fetcher_country = FETCHER[country_place]
                fetcher_names.extend(fetcher_country[type_place])
            except KeyError:
                pass

            log("DEBUG_0007", f"fetchers : {fetcher_names}")
            place = None
            while fetcher_names:
                fetcher_name = fetcher_names.popleft()
                log("DEBUG_0003", f"Running fetcher : {fetcher_name}")
                fetcher = self.FETCHER_DICT[fetcher_name]()
                try:
                    place = fetcher.fetch(userplace)
                except PlaceNotFoundError:
                    log("WARNIG_0001", f"Unable to find the place {userplace.name}")
                    continue
                if place:
                    userplace.place_id = place.id
                    userplace.type_place = place.type_place
                    userplace.update()
                    place.save()
                    if fetcher_country and type_place != place.type_place:
                        type_place = place.type_place
                        log("INFO_0010", f"Queue fetcher {fetcher_country[type_place]} because type_place {type_place} detected")
                        fetcher_names.extend(fetcher_country[type_place])
            self.output_data.append(place)
        return [n.to_dict() for n in self.output_data if n is not None]
