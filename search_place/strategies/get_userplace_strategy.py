
from search_place.strategies.strategy import Strategy

from search_place.data.user_place import UserPlace
from search_place.error.not_found_error import PlaceNotFoundError


class GetUserPlaceStrategy(Strategy):
    def load_data(self):
        self.data = None

    def write_data(self):
        pass

    def process(self, userplace_id):
        userplace = UserPlace.find_by_id(userplace_id)
        if userplace is None:
            raise PlaceNotFoundError(f"Unable to find userplace with id : {userplace_id}")

        return userplace.to_dict(resolv_dependency=True)
