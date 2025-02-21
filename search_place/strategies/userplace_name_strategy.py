from search_place.strategies.strategy import Strategy

from search_place.data.user_place import UserPlace
from search_place.error.not_found_error import ParamNotFoundError


class UserPlaceNameStrategy(Strategy):
    def load_data(self):
        # Pas de données en entrée. Uniquement au moment de l'execution
        self.data = None

    def write_data(self):
        self.data.save()

    def process(self, request_data):
        type_place = request_data.get("type_place", None)
        description = request_data.get("description", None)
        try:
            self.data = UserPlace.creater(name=request_data["name"], description=description, country=request_data["country"], type_place=type_place)
        except KeyError as e:
            raise ParamNotFoundError(f"Param {e} not found on data request")
        return self.data.to_dict()
