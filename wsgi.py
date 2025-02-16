import click, sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo('wash car'))
  #task 3
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database intialized')

#task 4.1
@app.cli.command("get-user", help="Retrieve a User")
@click.argument('username', default='bob')
def get_user(username):
  bob=User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found..')
    return
  print(bob)

#task 4.2
@app.cli.command("get-users")
def get_users():
  users=User.query.all()
  print(users)

#task 5
@app.cli.command("change-email")
@click.argument('username',default='bob')
@click.argument('email',default='bob@mail.com')
def change_email(username, email):
  bob=User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found..')
    return
  bob.email=email
  db.session.add(bob)
  db.session.commit()
  print(bob)

#task 6
"""
@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    
    db.session.rollback()
   
    print("Username or email already taken!") 
  else:
    print(newuser)
"""

@app.cli.command("create-user")
@click.argument('username',default='besty')
@click.argument('email', default='besty30@mail.com')
@click.argument('password',default='betsyboo')
def create_user(username,email,password):
  newuser=User(username,email,password)
  try:
    db.session.add(newuser)
    db.session.commit()
    #exception handling
  except IntegrityError as e:
    db.session.rollback()

    print("Username or email already taken")
  else:
    print(newuser)

#task 7
@app.cli.command("delete-user")
@click.argument('username',default='bob')
def delete_user(username):
  bob=User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found')
    return
  db.session.delete(bob)
  db.session.commit
  print(f'{username} has been deleted')

#task 8.4
@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  print(bob.todos)

#task 9.1
@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  new_todo = Todo(text)
  bob.todos.append(new_todo)
  db.session.add(bob)
  db.session.commit()

#task 9.2
@app.cli.command('toggle-todo')
@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')

@app.cli.command('add-category', help="Adds a category to a todo")
@click.argument('username', default='bob')
@click.argument('todo_id', default=6)
@click.argument('category', default='chores')
def add_todo_category_command(username, todo_id, category):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  res = user.add_todo_category(todo_id, category)
  if not res:
    print(f'{username} has no todo id {todo_id}')
    return

  print('Category added!')