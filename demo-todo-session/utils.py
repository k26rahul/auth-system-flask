import string
import secrets


def generate_token(length=10):
  chars = string.ascii_letters + string.digits
  return ''.join(secrets.choice(chars) for _ in range(length))
