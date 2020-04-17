from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, insert
from decorators import test_decorator
from settings import engine
import login
from gameplay import fetch_next_card
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


# ANCHOR COUNT_RIGHT
# this method updates the card's right answer number +1, it's level + 1 and updates the time it
# can be shown again.
@app.route('/count_right/<int:card_id>')
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
    return render_template('edit', message=f'Loading card id: {card_id}', card_data=card_data)
  else:
    # create new card
    return render_template('edit', message='Creating new card.')

# ANCHOR NEXT-CARD
@app.route('/next-card')
def next_card():
  with engine.connect() as con:
    user_id = 1
    res = con.execute(f'SELECT * FROM `cards` WHERE uid IN(\'{user_id}\');')
    cards = []
    play_card = {}
    for row in res:
      cards.append(dict(row))
    if len(cards) == 0:
      cards_status = 0 # for now cards status will help us determine if there are no cards at all, or just not for today (card_status = -1)
    else:
      play_card = cards[0]
      cards_status = play_card['card_id']
    # In no cards available for the user to display
    if cards_status == 0:
      return render_template('game.html', cards=0)
    elif cards_status == -1: # If no cards available for today, show, no more cards for today. Create a new card or come back tomorrow.
      return render_template('game.html', cards=-1)
    else:
      # otherwise load the first card from db and pass it to game template
      card_data = {
              'card_id': play_card['card_id'], 
              'text_front': play_card['text_front'],
              'image_front_url': play_card['image_front_url'],
              'text_back': play_card['text_back'],
              'image_back_url': play_card['image_back_url']
              }
      return render_template('game.html', card_data=card_data)


# ANCHOR SUBMIT CARD TO DB
@app.route('/submit_new_card')
def submit_new_card():
  print('Submitting new card')

    # NEXT TO DO
    # get-next-card - automate in a function
    # keep logged in user in a global