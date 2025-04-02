from search_place.strategies.strategy import Strategy
from search_place.utils.rest_countries_utils import RestCountriesUtils

from search_place.data.country import Country


class InitCountriesStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self):
        if Country.is_empty():
            countries = RestCountriesUtils.get_countries()
            Country.insert_many(countries)
