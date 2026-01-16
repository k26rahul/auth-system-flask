import json
import base64
import hmac
import hashlib
import time

SECRET = b'super-secret-key'

print("jwt.py file is being executed...")

# --- helpers ---


def b64url_encode(data: bytes) -> str:
  return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def b64url_decode(data: str) -> bytes:
  r = len(data) % 4
  if r > 0:
    data += '='*(4-r)
  return base64.urlsafe_b64decode(data)


def sign(message: bytes) -> str:
  sig = hmac.new(SECRET, message, hashlib.sha256).digest()
  return b64url_encode(sig)

# --- jwt core logic ---


def jwt_encode(payload: dict) -> str:
  header = {
      "alg": "HS256",
      "typ": "JWT",
  }

  header_b64 = b64url_encode(json.dumps(header).encode())
  payload_b64 = b64url_encode(json.dumps(payload).encode())

  message = f'{header_b64}.{payload_b64}'.encode()
  signature = sign(message)

  return f'{header_b64}.{payload_b64}.{signature}'


def jwt_decode(token: str) -> dict:
  header_b64, payload_b64, signature = token.split('.')

  message = f'{header_b64}.{payload_b64}'.encode()
  expected_signature = sign(message)

  if not hmac.compare_digest(signature, expected_signature):
    raise Exception("Invalid signature")

  return json.loads(b64url_decode(payload_b64))
