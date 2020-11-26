from enum import Enum


class ProjectPrivilegeTypesEnum(Enum):

    OWNER = 100
    ADMIN = 50
    READ_WRITE = 20
    READ_ONLY = 10
