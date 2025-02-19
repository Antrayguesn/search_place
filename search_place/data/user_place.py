import uuid
import datetime

from search_place.data.model import Model
from search_place.data.place import Place


class UserPlace(Model):
    def __init__(self,
                 name: str = None,
                 description: str = None,
                 country: str = None,
                 place_id=None,
                 type_place: str = None,
                 created_time=None,
                 last_update=None,
                 id=None,
                 **kwargs):
        super().__init__()
        self.name = name
        self.description = description
        self.country = country
        self.id = id
        self.type_place = type_place
        self.created_time = created_time
        self.last_update = last_update
        self.place_id = place_id

    @property
    def place(self):
        if self.place_id:
            return Place.find_by_id(self.place_id)
        else:
            return None

    @place.setter
    def place(self, place_id):
        if place_id:
            self._place = Place.find_by_id(place_id)
        else:
            self._place = None

    @classmethod
    def create_new_place_user(cls, name: str, description: str, country: str, type_place: str, place_id: str = None):
        created_time = datetime.datetime.now().timestamp()
        id_ = uuid.uuid4()

        user_place = UserPlace(name=name,
                               description=description,
                               country=country,
                               type_place=type_place,
                               created_time=created_time,
                               last_update=created_time,
                               place_id=place_id,
                               id=str(id_))

        return user_place

    def to_dict(self, resolv_dependency: bool = False):
        ret = {"name": self.name,
               "description": self.description,
               "id": self.id,
               "country": self.country,
               "type_place": self.type_place,
               "created_time": self.created_time,
               "last_update": self.last_update}

        if self.place_id and resolv_dependency:
            ret["place"] = self.place.to_dict()
        else:
            ret["place_id"] = self.place_id

        return ret
