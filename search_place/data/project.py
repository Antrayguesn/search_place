import datetime

from search_place.error.not_found_error import NotFoundError
from search_place.data.model import Model

from search_place.data.user_place import UserPlace


class Project(Model):
    PROPERTIES = ["id", "_id", "name", "created_time", "last_update", "user_place_id"]

    def __init__(self, **kwargs):
        self.user_places_id = []
        super().__init__(**kwargs)

    @property
    def user_places(self):
        userplaces = [UserPlace.find_by_id(up).to_dict(resolv_dependency=True) for up in self.user_places_id]
        return userplaces

    def add_userplace(self, userplace_id):
        self.user_places.append(userplace_id)
        self.last_update = datetime.datetime().timestamp()

    def remove_userplace(self, userplace_id):
        try:
            del self.user_places[userplace_id]
        except KeyError as e:
            raise NotFoundError(e)
        self.last_update = datetime.datetime().timestamp()

    def create_userplace(self, name: str, country: str, description: str = None, type_place: str = None):
        new_userplace = UserPlace.create(name=name, country=country, description=description, type_place=type_place)
        new_userplace.save()
        self.user_places_id.append(new_userplace.id)
        self.last_update = datetime.datetime.now().timestamp()
        self.update()

    def to_dict(self, resolv_dependency=False):

        ret = {
            "created_time": self.created_time,
            "last_update": self.last_update,
            "id": self.id,
            "name": self.name,
        }

        if resolv_dependency:
            ret["user_places"] = self.user_places
        else:
            ret["user_places_id"] = self.user_places_id

        return ret
