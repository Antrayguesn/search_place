import requests
import os

API_ALL_TRACKS = "https://api.doc.govt.nz/v1/tracks"
API_ALL_HUTS = "https://api.doc.govt.nz/v2/huts"
API_DETAIL_HUT = "https://api.doc.govt.nz/v2/huts/{id}/detail"
API_DETAIL_TRACK = "https://api.doc.govt.nz/v1/tracks/{id}/detail"


class DOCScrapAPIUtils():
    @staticmethod
    def scrap_tracks():
        token = os.environ.get("SP_DOC_API_TOKEN")
        res = requests.get(API_ALL_TRACKS, headers={"accept": "application/json", "x-api-key": token})
        res_json = res.json()

        return [{"doc_id": r["assetId"], "name": r["name"].strip()} for r in res_json]

    @staticmethod
    def scrap_huts():
        token = os.environ.get("SP_DOC_API_TOKEN")
        res = requests.get(API_ALL_HUTS, headers={"accept": "application/json", "x-api-key": token})
        res_json = res.json()

        return [{"doc_id": r["assetId"], "name": r["name"].strip()} for r in res_json]

    def hut_detail(hut_id):
        token = os.environ.get("SP_DOC_API_TOKEN")
        res = requests.get(API_DETAIL_HUT.format(id=hut_id), headers={"accept": "application/json", "x-api-key": token})
        res_json = res.json()
        return res_json

    def track_detail(track_id):
        token = os.environ.get("SP_DOC_API_TOKEN")
        res = requests.get(API_DETAIL_TRACK.format(id=track_id), headers={"accept": "application/json", "x-api-key": token})
        res_json = res.json()
        return res_json
