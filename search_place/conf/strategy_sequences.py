# Request's data are passed by the request_data arg

# Strategies run when the app is started
INIT_STRATEGIES = ["InitCountriesStrategy", "InitDOCTracksCollectionStrategy", "InitDOCHutsCollectionStrategy"]


SEQUENCES = {
    "GET": {
        "/get_userplace/<string:userplace_id>": {
            "STRATEGIES": [
                {"GetUserPlaceStrategy": ["userplace_id"]}

            ]
        },
        "/project/<string:project_id>": {
            "STRATEGIES": [
                {"GetProjectStrategy": ["project_id"]}
            ]
        },
        "/type/<string:country_name>": {
            "STRATEGIES": [
                {"GetTypeByCountryStrategy": ["country_name"]}
            ]
        },
        "/countries": {
            "STRATEGIES": [
                "GetCountriesStrategy"
            ]
        }

    },
    "POST": {
        "/fetch_place_data": {
            "STRATEGIES": [
                "FetcherStrategy"
            ]
        },
        "/place_name": {
            "STRATEGIES": [
                {"UserPlaceNameStrategy": ["request_data"]}
            ]
        },
        "/userplace/<string:userplace_id>": {
            "STRATEGIES": [
                {"UpdateUserPlaceStrategy": ["userplace_id", "request_data"]}
            ]
        },
        "/project/<string:project_name>": {
            "STRATEGIES": [
                {"ProjectStrategy": ["project_name"]}
            ]
        },
        "/project/<string:project_id>/userplace": {
            "STRATEGIES": [
                {"CreateUserPlaceInProjectStrategy": ["project_id", "request_data"]}
            ]
        }
    },
}
