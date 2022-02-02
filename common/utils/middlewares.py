from flask import request, g
from common.utils.jwt import verify_jwt


def token_validation():

    g.user_id = None

    token = request.headers.get('Authorization')
    if token is not None and token.startswith('Bearer '):

        token = token[7:]

        payload = verify_jwt(token)

        if payload is not None:
            g.user_id = payload.get('user_id')
