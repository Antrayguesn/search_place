import requests

API_URL_NOMINATIM = "https://nominatim.openstreetmap.org/search.php?street={place}&country={country}&format=jsonv2&extratags=1&addressdetails=1"


class NominatimSearchUtils:

    @staticmethod
    def nomincatim_search(place, country):
        req = requests.get(API_URL_NOMINATIM.format(place=place, country=country), headers={"User-agent": "classify - v0.1", "Accept-Language": "fr-FR, en;q=0.8"})
        res = req.json()
        print(res)
        if len(res) == 0:
            return None
        data = {}
        place_info = res[0]
        data['latitude'] = place_info["lat"]
        data['longitude'] = place_info["lon"]
        data['name'] = place_info["name"]
        data['link'] = place_info["extratags"]["website"]
        data['wikipedia'] = place_info["extratags"]["wikipedia"]
        return data
