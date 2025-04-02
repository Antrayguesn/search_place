from search_place.strategies.strategy import Strategy
from search_place.data.DOCHut import DOCHut

from search_place.utils.DOC_scrap_api_utils import DOCScrapAPIUtils


class InitDOCHutsCollectionStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self):
        if DOCHut.is_empty():
            data = DOCScrapAPIUtils.scrap_huts()
            DOCHut.insert_many(data)
