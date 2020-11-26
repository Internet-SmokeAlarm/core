from .project import Project


class ProjectFactory:

    @staticmethod
    def create_project(id: str,
                       name: str,
                       description: str = "") -> Project:
        devices = dict()
        experiments = dict()
        members = dict()
        billing = dict()

        return Project(name,
                       id,
                       devices,
                       experiments,
                       members,
                       billing,
                       description)