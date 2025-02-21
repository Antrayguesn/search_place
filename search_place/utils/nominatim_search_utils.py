import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search.php?street={place}&country={country}&format=jsonv2&extratags=1&addressdetails=1&layer=poi,address"

API_OSM_WAY = "https://www.openstreetmap.org/api/0.6/way/{osm_id}"


class NominatimSearchUtils:

    @staticmethod
    def nomincatim_search(place, country):
        req = requests.get(API_URL_NOMINATIM.format(place=place, country=country), headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
        res = req.json()
        if len(res) == 0:
            return None

        place_info = res[0]

        return place_info

    @staticmethod
    def osm_search(osm_id):
        req = requests.get(API_OSM_WAY.format(osm_id), headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
        res = req.text

        return res
