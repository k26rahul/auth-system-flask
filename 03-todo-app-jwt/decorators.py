from functools import wraps
from utils import validate_session
from flask import jsonify


def login_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    session = validate_session()
    if session:
      return fn(session, *args, **kwargs)
    else:
      return jsonify({"success": False, "message": "Unauthorized"}), 401

  return wrapper
