from search_place.strategies.strategy import Strategy

from search_place.data.project import Project

from search_place.error.not_found_error import ParamNotFoundError, ProjectNotFoundError


class CreateUserPlaceInProjectStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        self.project.save()

    def process(self, project_id, request_data):
        type_place = request_data.get("type_place", None)
        description = request_data.get("description", None)

        self.project = Project.find_by_id(project_id)
        if self.project is None:
            raise ProjectNotFoundError(f"Unable to find the project {project_id}")
        try:
            self.project.create_userplace(name=request_data["name"], description=description, country=request_data["country"], type_place=type_place)
        except KeyError as e:
            raise ParamNotFoundError(f"Param {e} not found on data request")

        return self.project.to_dict(resolv_dependency=True)
