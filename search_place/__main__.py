from flask import Flask, jsonify, request

from search_place.conf.strategy_sequences import SEQUENCES
from search_place.strategies.strategy_manager import StrategyManager

from search_place.error.not_found_error import NotFoundError
from search_place.services.mongodb_service import MongoDBService

import numpy as np


app = Flask(__name__)

strategy_manager = StrategyManager()
mongoDB = MongoDBService()
mongoDB.url = "mongodb://localhost:27017"
mongoDB.connect()

# Dynamic
for method, routes in SEQUENCES.items():
    for route, config in routes.items():
        strategies = config.get("STRATEGIES", [])

        def endpoint_function(route=route, strategies=strategies):
            def handler(**kwargs):
                args = np.array([list(s.values()) for s in strategies if type(s) is dict]).flatten().tolist()
                try:
                    if "request_data" in args:
                        response = strategy_manager.run_sequence(strategies, request_data=request.json, **kwargs)
                    else:
                        response = strategy_manager.run_sequence(strategies, **kwargs)
                    return jsonify(response)
                except NotFoundError as e:
                    return {"error": str(e)}, 404
            return handler
        endpoint_name = f"{method}_{route.replace('/', '_')}".strip('_')
        app.route(route, methods=[method], endpoint=endpoint_name)(endpoint_function())


if __name__ == "__main__":
    app.run()
