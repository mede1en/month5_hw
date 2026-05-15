import string

from django.core.cache import cache
import random

PREFIX = "confirmation_code"
TTL = 300

def _key(email):
    return f"{PREFIX}:{email}"

def set_confirmation_code():
    code = ''.join([str(random.randint(0, 9)) for i in range(6)])
    return code

def save_code_to_cache(email, code):
    key = _key(email)
    cache.set(key, code, TTL)

def verify_confirmation_code(email, code):
    key = _key(email)
    stored = cache.get(key)
    if stored and stored == code:
        return True
    return False
