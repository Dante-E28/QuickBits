TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'
EMAIL_VERIFICATION_TOKEN_TYPE = 'verification'
PASSWORD_RESET_TOKEN_TYPE = 'reset'

naming_convention = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s",
    }

# Expire time config.
SECONDS_IN_MINUTE = 60
SECONDS_IN_DAY = 86400
EMAIL_TOKEN_HOURS = 24
RESET_PASSWORD_TOKEN_HOURS = 1

# Server message type.
MESSAGE = 'message'
EXPIRE = 'expire'
