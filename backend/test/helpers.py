import random
import secrets
import string

from mimesis import Generic, Text
from mimesis.providers import BaseProvider


def generate_password(length=8):
    alphabet = string.ascii_letters + string.digits + \
               ''.join([x for x in string.punctuation if x not in '"\':;'])

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):

            if is_valid_password(password):
                return password


def is_valid_password(value):
    """ Password should be at least 8 characters and contain
    at least one digit and special character
    """

    allowed_special_characters = set('`~!@#$%^&*()_-+=[]\\}{][|,./><?')

    if len(value) < 8:
        return False

    contains_letter = any(c.isalpha() for c in value)
    contains_digit = any(c.isdigit() for c in value)
    contains_special_char = any(c in allowed_special_characters for c in value)

    return contains_letter and contains_digit and contains_special_char


class RegistrationDataGenerator(BaseProvider):
    class Meta:
        name = 'registration_set'

    def __call__(self, *args, **kwargs):
        t = Text()

        email = kwargs.pop('email', f'{t.word()}@example.com')
        username = kwargs.pop('username', email)
        password = kwargs.pop('password', generate_password())
        company = kwargs.pop('company', t.word())
        country = kwargs.pop('country', random.choice(kwargs.pop('countries', ['US'])))

        data = {
            'email': email,
            'username': username,
            'password': password,
            'company': company,
            'country': country,
            'tos': True,
            'marketing': False,
            'recaptcha': '1234567890'
        }

        data.update(kwargs)

        return data


g = Generic()
g.add_provider(RegistrationDataGenerator)
