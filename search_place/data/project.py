import datetime
import uuid

from search_place.error.not_found_error import NotFoundError
from search_place.data.model import Model

from search_place.data.user_place import UserPlace


class Project(Model):
    def __init__(self,
                 created_time: float = None,
                 last_update: float = None,
                 user_places_id: list = [],
                 name: str = None,
                 id=None,
                 **kwargs
                 ):
        super().__init__()
        self.created_time = created_time
        self.last_update = last_update
        self.user_places_id = user_places_id
        self.name = name
        self.id = id

    @property
    def user_places(self):
        print(self.user_places_id)
        return [UserPlace.find_by_id(up).to_dict(resolv_dependency=True) for up in self.user_places_id]

    @classmethod
    def create_new_project(cls, name: str):
        now_time = datetime.datetime.now().timestamp()
        project = Project(id=str(uuid.uuid4()),
                          created_time=now_time,
                          last_update=now_time,
                          name=name)
        return project

    def add_userplace(self, userplace_id):
        self.user_places.append(userplace_id)
        self.last_update = datetime.datetime().timestamp()

    def create_userplace(self, name: str, country: str, description: str = None, type_place: str = None):
        new_userplace = UserPlace.create_new_place_user(name=name, country=country, description=description, type_place=type_place)
        new_userplace.save()
        self.user_places_id.append(new_userplace.id)
        self.last_update = datetime.datetime.now().timestamp()
        self.update()

    def remove_userplace(self, userplace_id):
        try:
            del self.user_places[userplace_id]
        except KeyError as e:
            raise NotFoundError(e)
        self.last_update = datetime.datetime().timestamp()

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
