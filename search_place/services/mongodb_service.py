from search_place.services.service import Service

from pymongo import MongoClient


class MongoDBService(Service):
    def __init_(self):
        self.connection = None
        self._url = None
        self.collection = None
        self.__client = None
        self.db = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def connect(self):
        # Connexion à MongoDB
        self.__client = MongoClient(self.url)
        self.db = self.__client["search_place_db"]
