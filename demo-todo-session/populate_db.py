from models import db, User, Todo
from werkzeug.security import generate_password_hash


def populate_db():
  if User.query.count() > 0:
    return

  user1 = User(
      name="rahul",
      email="rahul@example.com",
      password=generate_password_hash('12345')
  )

  user2 = User(
      name="vidu",
      email="vidu@example.com",
      password=generate_password_hash('12345')
  )

  db.session.add_all([user1, user2])

  db.session.add(Todo(text="this is todo 1", user_id=1, is_done=True))
  db.session.add(Todo(text="this is todo 2", user_id=1, is_done=True))
  db.session.add(Todo(text="this is todo 3", user_id=1, is_starred=True))
  db.session.add(Todo(text="this is todo 4", user_id=1))
  db.session.add(Todo(text="this is todo 5", user_id=1))

  db.session.commit()
