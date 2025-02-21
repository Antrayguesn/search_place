from search_place.data.model import Model
from search_place.data.type.hut import Hut
from search_place.data.type.track import Track
from search_place.data.type.type import Type


class Place(Model):
    PROPERTIES = ["id", "name", "description", "latitude", "longitude", "image_link", "source_name", "source_url", "link", "wikipedia", "type_attr", "type_place", "country"]

    TYPE_PROPERTIES = {
        "wilderness_hut": Hut,
        "track": Track
    }

    def __init__(self, **kwargs):
        self.type_place = kwargs.get("type_place", None)
        super().__init__(**kwargs)
        self._type_attr = kwargs.get("type_attr", None)

    @property
    def type_attr(self):
        if isinstance(self._type_attr, Type):
            return self._type_attr

        if self.type_place and self.type_place in self.TYPE_PROPERTIES:
            self._type_attr = self.TYPE_PROPERTIES[self.type_place](**self._type_attr or {})
            return self._type_attr

        return None

    @type_attr.setter
    def type_attr(self, value):
        if value is None:
            self._type_attr = None
        elif isinstance(value, dict) and self.type_place in self.TYPE_PROPERTIES:
            self._type_attr = self.TYPE_PROPERTIES[self.type_place](**value)
        elif isinstance(value, Type):
            self._type_attr = value
        else:
            raise TypeError(f"type_attr doit être un dictionnaire ou un objet de type {Type}")

    def to_dict(self):
        data = {key: getattr(self, key, None) for key in self.__class__.PROPERTIES}

        if data["type_attr"]:
            data["type_attr"] = self.type_attr.to_dict()

        return data
