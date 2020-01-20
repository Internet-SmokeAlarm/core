from enum import Enum

class PermissionsGroupTypeEnum(Enum):

    USER = "USER"

    GROUP_ADMIN = "ADMIN"
    GROUP_MEMBER = "MEMBER"
    GROUP_READ_ONLY_MEMBER = "READ_ONLY_MEMBER"
    GROUP_DEVICE = "DEVICE"

    UNAUTHENTICATED = "UNAUTHENTICATED"
