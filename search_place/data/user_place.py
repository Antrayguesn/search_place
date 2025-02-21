from search_place.data.model import Model
from search_place.data.place import Place

from search_place.error.not_found_error import PlaceNotFoundError


class UserPlace(Model):
    PROPERTIES = ["id", "name", "description", "country", "type_place", "place_id", "created_time", "last_update", "_id"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def place(self):
        if self.place_id:
            place = Place.find_by_id(self.place_id)
            if place is None:
                raise PlaceNotFoundError(f"Unable to find place {self.place_id} in the database")
            return place
        else:
            return None

    @place.setter
    def place(self, place_id):
        pass

    def to_dict(self, resolv_dependency: bool = False):
        ret = {"name": self.name,
               "description": self.description,
               "id": self.id,
               "country": self.country,
               "type_place": self.type_place,
               "created_time": self.created_time,
               "last_update": self.last_update}

        if self.place_id is not None and resolv_dependency:
            ret["place"] = self.place.to_dict()
        else:
            ret["place_id"] = self.place_id

        return ret
