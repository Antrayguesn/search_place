from search_place.strategies.userplace_name_strategy import UserPlaceNameStrategy
from search_place.strategies.fetcher_strategy import FetcherStrategy
from search_place.strategies.get_userplace_strategy import GetUserPlaceStrategy
from search_place.strategies.project.get_project_strategy import GetProjectStrategy
from search_place.strategies.project.project_strategy import ProjectStrategy
from search_place.strategies.project.create_userplace_in_project_strategy import CreateUserPlaceInProjectStrategy
from search_place.strategies.DOCAPI.init_DOC_tracks_collection_strategy import InitDOCTracksCollectionStrategy
from search_place.strategies.DOCAPI.init_DOC_huts_collection_strategy import InitDOCHutsCollectionStrategy
from search_place.strategies.init_countries_strategy import InitCountriesStrategy
from search_place.strategies.get_type_by_country_strategy import GetTypeByCountryStrategy
from search_place.strategies.get_enum.get_countries_strategy import GetCountriesStrategy
from search_place.strategies.update_userplace_strategy import UpdateUserPlaceStrategy

from search_place.utils.singleton import Singleton
from search_place.data.log import log, INFO_END_PROCESS, INFO_LOADING_DATA, INFO_RUN_STRATEGIES


class StrategyManager(metaclass=Singleton):
    def __init__(self):
        self.SERVICE_CODE = "100"
        self.STRATEGIES = {UserPlaceNameStrategy.__name__: UserPlaceNameStrategy,
                           FetcherStrategy.__name__: FetcherStrategy,
                           GetUserPlaceStrategy.__name__: GetUserPlaceStrategy,
                           ProjectStrategy.__name__: ProjectStrategy,
                           GetProjectStrategy.__name__: GetProjectStrategy,
                           CreateUserPlaceInProjectStrategy.__name__: CreateUserPlaceInProjectStrategy,
                           InitDOCTracksCollectionStrategy.__name__: InitDOCTracksCollectionStrategy,
                           InitDOCHutsCollectionStrategy.__name__: InitDOCHutsCollectionStrategy,
                           InitCountriesStrategy.__name__: InitCountriesStrategy,
                           GetCountriesStrategy.__name__: GetCountriesStrategy,
                           GetTypeByCountryStrategy.__name__: GetTypeByCountryStrategy,
                           UpdateUserPlaceStrategy.__name__: UpdateUserPlaceStrategy
                           }

    def run_sequence(self, sequence, **kwargs):
        log(INFO_RUN_STRATEGIES, f"Run strategies {sequence}", self.SERVICE_CODE)

        log(INFO_LOADING_DATA, "Loading data ...", "000")

        return_strategy = None
        strategy_running = None

        for strategy in sequence:
            if type(strategy) is dict:
                for strat, args in strategy.items():
                    strategy_running = self.STRATEGIES[strat]
                    try:
                        params = {arg: kwargs[arg] for arg in args}
                        return_strategy = strategy_running().run(**params)
                    except KeyError as e:
                        log("ERROR_0002", f"Can found arg {e}", "000")
                        raise KeyError

            elif type(strategy) is str:
                strategy_running = self.STRATEGIES[strategy]
                return_strategy = strategy_running().run()
            else:
                log("ERROR_0001", "Paramater not reconized {strategy}", self.SERVICE_CODE)

        log(INFO_END_PROCESS, "End of process", "000")
        return return_strategy
