from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import check_password_hash
from models import db, User, Session, Todo
from utils import generate_token

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
  return render_template("index.html")


@routes.route("/auth/login", methods=["POST"])
def login():
  email = request.json.get('email')
  password = request.json.get('password')

  user = User.query.filter_by(email=email).first()

  if user and check_password_hash(user.password, password):
    session = Session(
        token=generate_token(),
        user_id=user.id
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Logged in as {user.name}',
        'payload': {
            'session_id': session.id,
            'token': session.token,
            "user_id": user.id
        }
    })
  else:
    return jsonify({
        'success': False,
        'message': f'Email or password incorrect',
    })


@routes.route("/todo/list")
def list_todos():
  session_id = request.args.get('session_id')
  token = request.args.get('token')

  session = Session.query.filter_by(id=session_id).first()

  if not session or session.token != token:
    return jsonify({"success": False, "message": "Invalid session"}), 401

  todos = Todo.query.filter_by(user_id=session.user_id).all()

  return jsonify({
      "success": True,
      "message": "All todos fetched",
      "payload": [
          {
              "text": todo.text,
              "is_done": todo.is_done,
              "is_starred": todo.is_starred,
          } for todo in todos
      ]
  })


@routes.route("/todo/create")
def create_todo():
  ...


@routes.route("/todo/update")
def update_todo():
  ...


@routes.route("/todo/delete")
def delete_todo():
  ...
