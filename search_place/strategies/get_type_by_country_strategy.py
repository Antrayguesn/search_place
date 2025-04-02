from search_place.strategies.strategy import Strategy
from search_place.data.place import Place


class GetTypeByCountryStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self, country_name):
        type_places = Place.distinct("type_place", {"country": country_name})
        return type_places
