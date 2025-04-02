
from search_place.strategies.strategy import Strategy
from search_place.data.country import Country


class GetCountriesStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self):
        countries = Country.find({})
        return [c.name["common"] for c in countries if c]
