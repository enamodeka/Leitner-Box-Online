from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, insert
from decorators import test_decorator
from settings import engine, settings, USER_ID
import login
from gameplay import fetch_next_card, add_card_to_db
import pprint
# import flask-sqlalchemy

app = Flask(__name__)
app_name = 'Leitner Box Online'

with engine.connect() as con:
  rs = con.execute('SELECT * FROM users')
  for row in rs:
    print('User: ', row)

# ANCHOR LOGIN
@app.route('/')
@test_decorator
def show_login_view():
    return render_template('login.html')

@app.route('/perform_login', methods=['POST'])
def perform_login():
  if(login.perform_login() == True):
    next_card = fetch_next_card()
    print(next_card)
    if(next_card['card_id'] == 0):
      return render_template('game.html', cards=0)
    elif(next_card['card_id'] == -1):
      return render_template('game.html', cards=-1)
    else:
    # return render_template with new card details
      return render_template('game.html', card_data=next_card)
  else:
    error_block = '<div class="form__error">Username or password are incorrect.</div>'
    return render_template('login.html', error_block=error_block)

# ANCHOR LOGOUT
@app.route('/logout')
def logout():
  settings[USER_ID] = 0
  return redirect('/')


# ANCHOR COUNT-RIGHT
# this method updates the card's right answer number +1, it's level + 1 and updates the time it
# can be shown again.
@app.route('/count-right/<int:card_id>')
def count_right(card_id):
  # load the card from DB
  with engine.connect() as con:
    res = con.execute(f'SELECT 1 FROM `cards` WHERE card_id IN(\'{card_id}\');')
    # check its level and update +1
    card = {}
    for row in res:
      card = dict(row)
    # check its correct answers and update + 1
    return redirect('/next-card')
    # take current timestamp and update it by day * level

# ANCHOR EDIT VIEW
# EDIT VIEW
@app.route('/edit/<int:card_id>')
def edit(card_id):
  if card_id != 0: 
    # fetch that card
    card_data = {
                'text_front': '',
                'img_front_url': '',
                'text_back': '',
                'img_back_url': '/static/back_1.png'
                }
    return render_template('edit.html', message=f'Loading card id: {card_id}', card_data=card_data, card_id=card_id)
  else:
    # create new card
    return render_template('edit.html', message='Creating new card.', card_id=card_id)

# ANCHOR NEXT-CARD
@app.route('/next-card')
def next_card():
  pass


# ANCHOR SUBMIT CARD TO DB
@app.route('/add-card', methods=['POST'])
def add_card_to_deck():
  data = request.get_json()
  print('Received data', data)
  add_card_to_db(data)
  # THIS IS NOT DOING ANYTHING? MANUALLY REDIRECTING TO THIS ROUTE IN JS
  return render_template('card-added.html')
    # NEXT TO DO
    # get-next-card - automate in a function
    # keep logged in user in a global

@app.route('/card-added')
def card_added_to_deck():
  return render_template('card-added.html')
