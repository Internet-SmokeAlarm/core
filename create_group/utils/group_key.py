import uuid

def generate_group_key(group_name):
    """
    Generates a unique group key using the group name.

    :param group_name: Group Name
    :type group_name: str
    """
    group_uuid = str(uuid.uuid4())

    return group_name + "-" + group_uuid
