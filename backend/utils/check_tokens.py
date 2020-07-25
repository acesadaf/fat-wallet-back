from backend.models import *
from django.contrib.auth.models import User


def valid_token(body):
    username, given_token = body["username"], body["token"]
    user = User.objects.get(username=username)
    ut = user_tokens.objects.get(user=user)
    token = ut.token
    if not given_token.isnumeric():
        return False
    return int(given_token) == token
