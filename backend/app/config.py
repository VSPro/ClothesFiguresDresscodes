import os
import sys
import logging
logger = logging.getLogger()

class Config(object):
    required_keys = [
        'USER_EMAIL_SENDER_EMAIL',
        'SECRET_KEY',
        'DB_HOST',
        'DB_PORT',
        'DB_USERNAME',
        'DB_PASSWORD',
        'DB_DATABASE',
        'USER_EMAIL_SENDER_NAME',
      ]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "Workshop"
    # otherwise we try to use sessions which is bad
    USER_ENABLE_REMEMBER_ME = False
    USER_AUTO_LOGIN_AFTER_CONFIRM = False
    USER_AUTO_LOGIN_AFTER_REGISTER = True
    # only for dev, prevents caching of static resources
    SEND_FILE_MAX_AGE_DEFAULT = 0
    USER_RESET_PASSWORD_URL = '/reset-confirmation'

    def __init__(self):
        for k in self.required_keys:
            v = os.environ.get(k, None)
            if v == 'True':
                v = True
            elif v == 'False':
                v = False
            elif isinstance(v, str) and v.isnumeric():
                v = int(v)
            setattr(self, k, v)

        for k in self.required_keys:
            if getattr(self, k, None) is None:
                logger.error("!!! Missing required config key '{}'.".format(k))

        dburi = "postgres://{}:{}@{}:{}/{}".format(
            getattr(self,'DB_USERNAME'),
            getattr(self,'DB_PASSWORD'),
            getattr(self,'DB_HOST'),
            getattr(self,'DB_PORT'),
            getattr(self,'DB_DATABASE')
        )
        setattr(self, 'SQLALCHEMY_DATABASE_URI', dburi)