from .permissions_group_types import PermissionsGroupTypeEnum

def get_resource_list(permissions_group_type, group_id, round_id, device_id):
    """
    :param permissions_group_type: PermissionsGroupTypeEnum
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return get_resource_method(permissions_group_type)(group_id, round_id, device_id)

def get_resource_method(permissions_group_type):
    if permissions_group_type == PermissionsGroupTypeEnum.GROUP_ADMIN:
        return get_group_admin_resource_list
    elif permissions_group_type == PermissionsGroupTypeEnum.GROUP_MEMBER:
        return get_group_member_resource_list
    elif permissions_group_type == PermissionsGroupTypeEnum.GROUP_READ_ONLY_MEMBER:
        return get_group_read_only_member_resource_list
    elif permissions_group_type == PermissionsGroupTypeEnum.GROUP_DEVICE:
        return get_group_device_resource_list
    elif permissions_group_type == PermissionsGroupTypeEnum.USER:
        return get_user_resource_list
    else:
        return get_default_resource_list

def get_user_resource_list(group_id, round_id, device_id):
    return [
        "v1/group/create",
        "v1/group/delete"
    ]

def get_group_admin_resource_list(group_id, round_id, device_id):
    """
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return [
        "v1/round/get/" + group_id + "/*",
        "v1/round/get/aggregate_model/" + group_id + "/*",
        "v1/round/get/start_model/" + group_id + "/*",
        "v1/round/start",

        "v1/group/get/" + group_id,
        "v1/group/get/current_round_id/" + group_id,
        "v1/group/get/initial_model/" + group_id,
        "v1/group/post/initial_model",

        "v1/device/get/active/" + device_id,
        "v1/device/register"
    ]

def get_group_member_resource_list(group_id, round_id, device_id):
    """
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return [
        "v1/round/get/" + group_id + "/*",
        "v1/round/get/aggregate_model/" + group_id + "/*",
        "v1/round/get/start_model/" + group_id + "/*",
        "v1/round/start",

        "v1/group/get/" + group_id,
        "v1/group/get/current_round_id/" + group_id,
        "v1/group/get/initial_model/" + group_id,
        "v1/group/post/initial_model",

        "v1/device/get/active/" + device_id,
        "v1/device/register"
    ]

def get_group_read_only_member_resource_list(group_id, round_id, device_id):
    """
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return [
        "v1/round/get/" + group_id + "/*",
        "v1/round/get/aggregate_model/" + group_id + "/*",
        "v1/round/get/start_model/" + group_id + "/*",

        "v1/group/get/" + group_id,
        "v1/group/get/current_round_id/" + group_id,
        "v1/group/get/initial_model/" + group_id,

        "v1/device/get/active/" + device_id
    ]

def get_group_device_resource_list(group_id, round_id, device_id):
    """
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return [
        "v1/round/get/" + group_id + "/*",
        "v1/round/get/start_model/" + group_id + "/*",

        "v1/device/get/active/" + device_id,
        "v1/submit_model_update",

        "v1/group/get/current_round_id/" + group_id
    ]

def get_default_resource_list(group_id, round_id, device_id):
    """
    :param group_id: string
    :param round_id: string
    :param device_id: string
    """
    return []
