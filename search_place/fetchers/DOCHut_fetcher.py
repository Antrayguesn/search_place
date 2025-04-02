from search_place.fetchers.fetcher import Fetcher

from search_place.data.DOCHut import DOCHut

from search_place.utils.DOC_scrap_api_utils import DOCScrapAPIUtils


class DOCHutFetcher(Fetcher):
    MATCHING_RULES = {
        "name": "name",
        "description": "introduction",
        "image_link": "introductionThumbnail",
        "link": "static_link"
    }
    MATCHING_TYPE_RULES = {
        "wilderness_hut": {
            "capacity": "numberOfBunks",
            "category": "hutCategory",
            "reservation": "bookable",
            "status": "status"
        }
    }

    def search(self, place_name, user_place):
        hut = DOCHut.find_one({"name": place_name})
        if not hut:
            return None
        return DOCScrapAPIUtils.hut_detail(hut.doc_id)
