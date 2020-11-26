from .user import User


class UserFactory:

    @staticmethod
    def create_user(username: str) -> User:
        projects = dict()
        api_keys = set()

        return User(username,
                    projects,
                    api_keys)