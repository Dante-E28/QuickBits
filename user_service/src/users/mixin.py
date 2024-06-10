import re
from pydantic import field_validator

from src.error_messages import (
    PASSWORD_INVALID_CHARACTER,
    PASSWORD_NO_CAPITAL_LETTER,
    PASSWORD_NO_DIGIT,
    USERNAME_INVALID_CHARACTER,
    USERNAME_TOO_SHORT
)
from src.exceptions import ValidationCustomError


class PasswordValidatorMixin:
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        if not re.match(r'^[a-zA-Z\d@$!%*?&]+$', password):
            raise ValidationCustomError(PASSWORD_INVALID_CHARACTER)
        if re.search(r'[A-Z]', password) is None:
            raise ValidationCustomError(PASSWORD_NO_CAPITAL_LETTER)
        if re.search('[0-9]', password) is None:
            raise ValidationCustomError(PASSWORD_NO_DIGIT)
        return password


class UsernameValidatorMixin:
    @field_validator('username')
    @classmethod
    def validate_username(cls, username: str):
        if re.fullmatch(r'[A-Za-z0-9_]*', username) is None:
            raise ValidationCustomError(USERNAME_INVALID_CHARACTER)
        if len(re.findall(r'[A-Za-z]', username)) < 4:
            raise ValidationCustomError(USERNAME_TOO_SHORT)
        return username
