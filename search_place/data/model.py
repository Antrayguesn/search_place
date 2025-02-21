import datetime
import uuid

from search_place.services.mongodb_service import MongoDBService
from search_place.data.type.type import Type
from search_place.data.log import log


class Model:
    PROPERTIES = []

    def __init__(self, **kwargs):
        self.db = MongoDBService().db
        self.collection = self.db[self.__class__.__name__.lower()]
        if self.__class__.PROPERTIES == "*":
            for key, value in kwargs.items():
                setattr(self, key, value)
        else:
            for key in self.__class__.PROPERTIES:
                setattr(self, key, kwargs.get(key, None))

    @classmethod
    def create(cls, **kwargs):
        create_time = datetime.datetime.now().timestamp()
        id_ = str(uuid.uuid4())
        return cls(**kwargs, created_time=create_time, last_update=create_time, id=id_)

    def save(self):
        if "_id" in self.__dict__ and self._id:
            self.update()
        else:
            inserted_id = self.collection.insert_one(self.to_dict())
            self._id = inserted_id

    @classmethod
    def insert_many(cls, data):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        collection.insert_many(data)

    @classmethod
    def is_empty(cls):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        is_empty = collection.count_documents({}) == 0
        return is_empty

    def merge(self, merging_type, force=False):
        """
        Met à jour les champs qui sont None avec les valeurs de l'autre instance.
        Si `force=True`, remplace même les valeurs existantes.
        """
        for key, value in merging_type.to_dict().items():
            attr = getattr(self, key, None)

            if isinstance(attr, Type):
                if value is None:
                    continue  # Ne rien faire si l'autre valeur est None

                if isinstance(value, dict):  # Convertir en Type si besoin
                    value = type(attr)(**value)

                if attr is None:  # Si `self.type_attr` est None, le créer
                    setattr(self, key, value)
                else:
                    attr.merge(value, force=True)
            elif force:
                if value is not None:
                    setattr(self, key, value)
            else:
                if attr is None and value is not None:
                    setattr(self, key, value)
        return self

    @classmethod
    def find_by_id(cls, id):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        document = collection.find_one({"id": id})
        if document is None:
            return None
        model = cls(**document)
        return model

    @classmethod
    def find_one(cls, query):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        document = collection.find_one(query)
        if document is None:
            return None
        model = cls(**document)
        return model

    @classmethod
    def find(cls, query):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        documents = collection.find(query)

        return [cls(**document) for document in documents]

    def update(self):
        log("DEBUG_0003", f"update {self.__class__.__name__} id: {self.id}", id_update=self.id)
        self.collection.update_one({"id": self.id}, {"$set": self.to_dict()})

    def to_dict(self):
        if self.__class__.PROPERTIES == "*":
            return vars(self)
        else:
            return {key: getattr(self, key, None) for key in self.__class__.PROPERTIES}

    def __repr__(self):
        return repr(self.to_dict())
