import base64
import hashlib
import hmac
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import caches

default_cache = caches['default']


class cached:
    def __init__(self, f, *args, **kwargs):
        self.default_cache = default_cache
        self.default_max_age = kwargs.get(
            "default_cache_max_age",
            int(settings.COTURN_EXPIRATION/2)
        )
        self.func = f

    def __call__(self, *args, **kwargs):
        user_id = kwargs.get("user_id", 0)
        if not user_id:
            return 0, 0
        value = self.get_from_cache_by_key(user_id)
        if value is not None:
            return value
        else:

            def inner(*args, **kwargs):
                value = self.func(*args, **kwargs)
                self.set_to_cache(user_id, value)
                return value
            return inner(*args, **kwargs)

    def get_from_cache_by_key(self, key):
        return self.default_cache.get(key)

    def set_to_cache(self, key, value):
        self.default_cache.add(key, value, self.default_max_age)


@cached
def get_coturn_credentials(user_id: str):
    now = datetime.utcnow()
    expiration_ts = (
        now + timedelta(seconds=settings.COTURN_EXPIRATION)
    ).timestamp()
    coturn_user = "{}:{}".format(int(expiration_ts), user_id)  # turn user
    token = hmac.new(
        settings.COTURN_SECRET.encode("utf-8"),
        coturn_user.encode("utf-8"),
        hashlib.sha1
    )
    coturn_encoded_token = base64.b64encode(token.digest()).decode("utf-8")  # turn password
    return {
        "username": coturn_user,
        "password": coturn_encoded_token
    }
