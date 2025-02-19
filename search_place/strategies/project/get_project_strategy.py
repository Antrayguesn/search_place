from search_place.strategies.strategy import Strategy

from search_place.data.project import Project

from search_place.error.not_found_error import ProjectNotFoundError


class GetProjectStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        pass

    def process(self, project_id):
        project = Project.find_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Unable to find the project {project_id}")
        return project.to_dict(resolv_dependency=True)
