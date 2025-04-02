from search_place.strategies.strategy import Strategy
from search_place.data.DOCTrack import DOCTrack

from search_place.utils.DOC_scrap_api_utils import DOCScrapAPIUtils


class InitDOCTracksCollectionStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self):
        if DOCTrack.is_empty():
            data = DOCScrapAPIUtils.scrap_tracks()
            DOCTrack.insert_many(data)
