import secrets
import base64
import json
from string import ascii_letters, digits
from flask import request
from models import Session


def generate_token(length=10):
  chars = ascii_letters + digits
  return ''.join(secrets.choice(chars) for _ in range(length))


def validate_session():
  session_cookie = request.cookies.get("session")
  if session_cookie:
    payload = json.loads(base64.urlsafe_b64decode(session_cookie).decode())

    session = Session.query.filter_by(id=payload["session_id"]).first()
    if session and session.token == payload["token"]:
      return session
  return None  # Unauthorized
