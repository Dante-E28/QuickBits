# Message type.
ERROR_MESSAGE = 'msg'

# Error messages for authentication and authorization
INVALID_CREDENTIALS = 'Неверное имя или пароль.'
INVALID_TOKEN = 'Неверный токен.'
INVALID_TOKEN_TYPE = 'Тип токена неверный: {token_type!r}.'
NOT_AUTHENTICATED = 'Не аутентифицирован.'
EMAIL_NOT_VERIFIED = 'Электронная почта не подтверждена.'
NOT_ACTIVE = 'Пользователь не активен.'
NOT_PRIVILEGES = 'Нет прав.'

# Entity error messages
USER_NOT_FOUND = 'User with data: {entity_data} not found.'
USER_ALREADY_EXISTS = 'Пользователь уже существует.'

# Validation error messages
PASSWORD_NO_CAPITAL_LETTER = 'В пароле должна быть заглавная буква.'
PASSWORD_NO_DIGIT = 'В пароле должна быть цифра.'
USERNAME_INVALID_CHARACTER = 'Недопустимы символ в юзернейме.'
USERNAME_TOO_SHORT = 'Букв побольше напиши (> 3).'
PASSWORD_INVALID_CHARACTER = (
    'Используйте в пароле латинские буквы, цифры и спецсимволы.')
INVALID_EMAIL = 'Неправильный формат электронной почты.'

# Email verification and password reset error messages
EMAIL_NOT_SENDING = (
    'Не удалось отправить письмо. Обратитесь к администратору.')
SMTP_SERVER_DOWN = (
    'Произошел сбой на сервере отправки писем. Попробуйте позже.')

# Limiter error messages
TOO_MANY_REQUESTS = 'Слишком много запросов.'
