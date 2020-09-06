from ....database import DB
from ....model import User
from ....model import DBObject


def handle_load_user(db: DB, username: str) -> User:
    """
    If the user exists, return them. Otherwise, create them
    and save to DB.
    """
    try:
        return DBObject.load_from_db(User, username, db)
    except:
        user = User(username, [], [])
        user.save_to_db(db)

        return user
