from enum import Enum


class Roles(Enum):
    ACTIVE = 'is_active'
    VERIFIED = 'is_verified'
    SUPERUSER = 'is_superuser'
