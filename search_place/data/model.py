from search_place.services.mongodb_service import MongoDBService
from search_place.data.log import log


class Model:
    def __init__(self, **kwargs):
        self.db = MongoDBService().db
        self.collection = self.db[self.__class__.__name__.lower()]

    def save(self):
        inserted_id = self.collection.insert_one(self.to_dict())
        self._id = inserted_id

    def merge(self, **kwargs):
        """
        Met à jour les champs qui sont None avec les valeurs de l'autre instance.
        """
        for key, value in kwargs.items():
            if getattr(self, key, None) is None and value is not None:
                setattr(self, key, value)

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
    def find(cls, query):
        db = MongoDBService().db
        collection = db[cls.__name__.lower()]
        documents = collection.find(query)

        return [cls(**document) for document in documents]

    def update(self):
        log("DEBUG_0003", f"update {self.__class__.__name__} id: {self.id}", id_update=self.id)
        self.collection.update_one({"id": self.id}, {"$set": self.to_dict()})
