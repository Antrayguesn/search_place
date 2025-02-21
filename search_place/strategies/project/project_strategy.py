from search_place.strategies.strategy import Strategy

from search_place.data.project import Project


class ProjectStrategy(Strategy):
    def load_data(self):
        pass

    def write_data(self):
        self.data.save()

    def process(self, project_name):
        self.data = Project.create(name=project_name)
        return self.data.to_dict(resolv_dependency=True)
