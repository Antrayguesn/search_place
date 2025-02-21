from search_place.data.place import Place
from search_place.error.not_found_error import PlaceNotFoundError


class Fetcher:
    MATCHING_RULES = {}
    MATCHING_TYPE_RULES = {}

    @staticmethod
    def get_nested_value(data, keys, default=None):
        """
        Récupère une valeur potentiellement imbriquée dans un dictionnaire.
        Exemple :
        data = {"extratags": {"website": "https://example.com"}}
        get_nested_value(data, ("extratags", "website")) → "https://example.com"
        """
        if isinstance(keys, str):
            return data.get(keys, default)

        result = data
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return default
        return result

    def search(place, userplace):
        pass

    def fetch(self, user_place):
        if user_place.place:
            print(user_place.place)
            place_name = user_place.place.name
        else:
            place_name = user_place.name

        info = self.search(place_name, user_place)
        if info is None:
            raise PlaceNotFoundError(f"Unable to find place {place_name}")

        data = {}
        data_type = None

        for key, value in self.__class__.MATCHING_RULES.items():
            data[key] = self.get_nested_value(info, value, None)

        try:
            str_type_place = data["type_place"]
        except KeyError:
            str_type_place = None

        if str_type_place is None:
            str_type_place = user_place.type_place

        if str_type_place and str_type_place in self.__class__.MATCHING_TYPE_RULES:
            matching_rules = self.MATCHING_TYPE_RULES[str_type_place]
            data_type = {}
            for key, value in matching_rules.items():
                data_type[key] = self.get_nested_value(info, value, None)

        if user_place.place:
            new_place = Place(**data)
            new_place.type_place = str_type_place
            if data_type:
                new_place.type_attr = data_type

            place = user_place.place.merge(new_place)
            return place

        place = Place.create(**data)
        if data_type:
            place.type_attr = data_type
        return place
