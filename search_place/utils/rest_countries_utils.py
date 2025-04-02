import requests

API_REST_COUNTRIES = "https://restcountries.com/v3.1/all?fields=name,flags,translations,cca3,cca2"


class RestCountriesUtils:
    @staticmethod
    def get_countries():
        ret = requests.get(API_REST_COUNTRIES)
        return ret.json()
