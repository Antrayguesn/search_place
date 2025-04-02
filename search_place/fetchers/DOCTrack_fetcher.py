from search_place.fetchers.fetcher import Fetcher

from search_place.data.DOCTrack import DOCTrack

from search_place.utils.DOC_scrap_api_utils import DOCScrapAPIUtils


class DOCTrackFetcher(Fetcher):
    MATCHING_RULES = {
        "name": "name",
        "description": "introduction",
        "image_link": "introductionThumbnail",
        "link": "static_link"
    }
    MATCHING_TYPE_RULES = {
        "track": {
            "distance": "distance",
            "walk_duration": "walkDuration",
            "walk_track_category": "walkTrackCategory",
            "kayakin_duration": "kayakinDuration"
        }
    }

    def search(self, place_name, user_place):
        track = DOCTrack.find_one({"name": place_name})
        if not track:
            return None
        track_info = DOCScrapAPIUtils.track_detail(track.doc_id)
        if "message" in track_info:
            return None
        if "walkTrackCategory" in track_info:
            track_info["walkTrackCategory"] = " / ".join(track_info["walkTrackCategory"])
        return track_info
