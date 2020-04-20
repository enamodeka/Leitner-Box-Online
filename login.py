from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, insert
from settings import settings, engine, USER_ID

def perform_login():
  username = request.form['username']
  password = request.form['password']

  # connect to DB and check if there is 'username' matches a value in
  # users['username'] and same for password
  with engine.connect() as con:
    
    does_user_exist = con.execute(f'SELECT * FROM users WHERE username IN(\'{username}\') AND password IN(\'{password}\');')
    user_exists_with_password = does_user_exist.fetchall() # returns result of the operation as a list
    user = user_exists_with_password[0]
    user_id = user[0]
    print('user id', user_id)
    settings[USER_ID] = user_id
    print('user id global', settings[USER_ID])

    if len(user_exists_with_password) != False:
      # Fetch a card
      print('Login successful')
      return True
    else:
     return False


# DECORATOR CHECKING IF THE USER IS LOGGED IN
# IF NOT IT REDIRECTS TO THE LOGIN SCREEN
def is_user_logged_in(func):
  @wraps(func)
  def wrap_func(*args, **kwargs):
    func(*args, **kwargs)
    if settings[USER_ID] == 0:
      pass
    return func(*args, **kwargs)
  return wrap_func