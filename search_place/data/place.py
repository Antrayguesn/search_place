import datetime
import uuid

from search_place.data.model import Model


class Place(Model):
    def __init__(self,
                 name: str = None,
                 description: str = None,
                 latitude: float = None,
                 longitude: float = None,
                 image_link: str = None,
                 last_update: float = None,
                 create_time: float = None,
                 link: str = None,
                 id=None,
                 source_url: str = None,
                 source_name: str = None,
                 wikipedia: str = None,
                 **kwargs
                 ):
        super().__init__()
        self.name = name
        self.description = description
        self.coord = (latitude, longitude)
        self.image_link = image_link
        self.last_update = last_update
        self.create_time = create_time
        self.link = link
        self.id = id
        self.source_url = source_url
        self.source_name = source_name
        self.wikipedia = wikipedia

    @staticmethod
    def create_new_place(latitude: float, longitude: float, name: str, description: str = "", image_link: str = "", link: str = "", source_url: str = None, source_name: str = None, wikipedia: str = None):
        create_time = datetime.datetime.now().timestamp()
        place = Place(latitude=latitude,
                      longitude=longitude,
                      description=description,
                      name=name,
                      image_link=image_link,
                      link=link,
                      create_time=create_time,
                      last_update=create_time,
                      id=str(uuid.uuid4()),
                      source_url=source_url,
                      source_name=source_name,
                      wikipedia=wikipedia
                      )
        return place

    def to_dict(self):
        return {"name": self.name,
                "description": self.description,
                "coord": self.coord,
                "image_link": self.image_link,
                "id": self.id,
                "last_update": self.last_update,
                "create_time": self.create_time,
                "source_url": self.source_url,
                "source_name": self.source_name,
                "link": self.link}
