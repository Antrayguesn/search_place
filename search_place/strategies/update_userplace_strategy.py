from search_place.strategies.strategy import Strategy

from search_place.data.user_place import UserPlace


class UpdateUserPlaceStrategy(Strategy):
    def load_data(self):
        # Pas de données en entrée. Uniquement au moment de l'execution
        self.data = None

    def write_data(self):
        self.data.save()

    def process(self, userplace_id, request_data):

        type_place = request_data.get("type_place", None)
        description = request_data.get("description", None)
        name_user_place = request_data.get("name", None)
        country = request_data.get("country", None)

        print(request_data)

        userplace = UserPlace.find_by_id(userplace_id)

        new_user_place = UserPlace.create(name=name_user_place, description=description, country=country, type_place=type_place)
        if userplace.place:
            userplace.place.place.id = None

        self.data = userplace.merge(new_user_place, force=True)
        print(self.data)

        return self.data.to_dict()
