# Error messages for authentication and authorization
INVALID_CREDENTIALS = 'Неверное имя или пароль.'
INVALID_TOKEN = 'Неверный токен.'
INVALID_TOKEN_TYPE = 'Тип токена неверный: {token_type!r}.'
NOT_AUTHENTICATED = 'Не аутентифицирован.'
EMAIL_NOT_VERIFIED = 'Электронная почта не подтверждена.'
NOT_ACTIVE = 'Пользователь не активен.'
USER_ALREADY_EXISTS = 'Пользователь уже существует.'
NOT_PRIVILEGES = 'Нет прав.'

# Entity error messages
ENTITY_NOT_FOUND = '{entity_type} id: {entity_id} не найден.'
ENTITY_ALREADY_EXISTS = '{entity_type} уже существует.'

# Validation error messages
PASSWORD_NO_CAPITAL_LETTER = 'В пароле должна быть заглавная буква.'
PASSWORD_NO_DIGIT = 'В пароле должна быть цифра.'
USERNAME_INVALID_CHARACTER = 'Недопустимы символ в юзернейме.'
USERNAME_TOO_SHORT = 'Букв побольше напиши (> 3).'
PASSWORD_INVALID_CHARACTER = (
    'Используйте в пароле латинские буквы, цифры и спецсимволы.')
