from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()

class TokenPayload:
  def __init__(self, payload):
    self.user_identifier = payload.get('user_identifier')
    self.exp = payload.get('exp')
    self.iat = payload.get('iat')
    self.username = payload.get('username')
    self.role = payload.get('role')

def verify_jwt(token):  # From : https://medium.com/codex/django-rest-framework-custom-jwt-authentication-backend-17bbd178b4fd
  # Decode the JWT and verify its signature
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return TokenPayload(payload)
  except jwt.exceptions.InvalidSignatureError:
    raise AuthenticationFailed('Invalid signature')
  except:
    raise ParseError()

def create_jwt(username, role):
  # Create the JWT payload
  payload = {
    'user_identifier': username,
    'exp': int((datetime.now() + timedelta(hours=settings.TOKEN_LIFETIME_HOURS)).timestamp()),
    # set the expiration time for 5 hour from now
    'iat': datetime.now().timestamp(),
    'username': username,
    'role': role,
  }
  # Encode the JWT with your secret key
  jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
  return jwt_token.decode('utf-8')