import re
from pydantic import field_validator


class PasswordValidatorMixin:
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        if re.search(r'[A-Z]', password) is None:
            raise ValueError('The password must contain a capital letter')
        if re.search('[0-9]', password) is None:
            raise ValueError('The password must contain a digit')
        return password


class UsernameValidatorMixin:
    @field_validator('username')
    @classmethod
    def validate_username(cls, username: str):
        if re.fullmatch(r'[A-Za-z0-9_]*', username) is None:
            raise ValueError('Invalid character in the username')
        if len(re.findall(r'[A-Za-z]', username)) < 4:
            raise ValueError('The number of characters must be more than 4')
        return username
