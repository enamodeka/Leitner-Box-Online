from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, insert
from settings import engine, settings, USER_ID
import login
from gameplay import fetch_next_card, add_card_to_db, update_card_in_db, count_update, fetch_all_cards_for_user, fetch_card, delete_card_in_db
import datetime
import arrow
import pprint
import os
import uuid
from werkzeug.utils import secure_filename
import json

# Meta
##################
__version__ = '0.1.0'

# Config
##################
BASE_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOAD_FOLDER = './static/uploads'# os.path.join(MEDIA_ROOT, 'upload')
ALLOWED_EXTENSIONS = {'jpg', 'png'}


app = Flask(__name__)
app_name = 'Leitner Box Online'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.run('0.0.0.0')

with engine.connect() as con:
  rs = con.execute('SELECT * FROM users')
  for row in rs:
    print('User: ', row)

# ANCHOR LOGIN
@app.route('/')
def show_login_view():
    return render_template('login.html')

@app.route('/perform_login', methods=['POST'])
def perform_login():
  if(login.perform_login() == True):
    return redirect ('/next-card')
  else:
    error_block = '<div class="form__error">Username or password are incorrect.</div>'
    return render_template('login.html', error_block=error_block)

# ANCHOR LOGOUT
@app.route('/logout')
def logout():
  settings[USER_ID] = 0
  return redirect('/')


# ANCHOR COUNT-RIGHT
# this method updates the card's right answer number +1, 
# its level + 1 and updates the time it can be shown again.
@app.route('/count-right/<int:card_id>')
@login.is_user_logged_in
def count_right(card_id):
    count_update(card_id, True)
    return redirect('/next-card')

# ANCHOR COUNT-WRONG    
@app.route('/count-wrong/<int:card_id>')
@login.is_user_logged_in
def count_wrong(card_id):
    count_update(card_id, False)
    return redirect('/next-card')


# ANCHOR EDIT VIEW
# EDIT VIEW
# TODO Make sure that the cards can be only edited by the logged in user
@app.route('/edit/<int:card_id>')
@login.is_user_logged_in
def edit(card_id):
  if card_id != 0: 
    # fetch that card
    card = fetch_card(card_id)
    print('Card fetched: ', card)
    return render_template('edit.html', message=f'Loading card id: {card_id}', card_data=card, card_id=card_id, view='edit')
  else:
    # create new card
    return render_template('edit.html', message='Creating new card.', card_id=card_id, view='create')
    
# ANCHOR DELETE
# EDIT VIEW
# TODO Make sure that the cards can be only deleted by the logged in user
@app.route('/delete/<int:card_id>')
@login.is_user_logged_in
def delete(card_id):
  delete_card_in_db(card_id)
  return redirect('/card-list')

# ANCHOR NEXT-CARD
@app.route('/next-card')
@login.is_user_logged_in
def next_card():
  next_card = fetch_next_card()
  print(next_card)
  if(next_card['card_id'] == 0):
    return render_template('game.html', cards=0, view='game')
  elif(next_card['card_id'] == -1):
    return render_template('game.html', cards=-1, view='game')
  else:
    return render_template('game.html', cards=1, card_data=next_card, view='game')


# ANCHOR SUBMIT CARD TO DB
@app.route('/add-card', methods=['POST', 'GET'])
# @login.is_user_logged_in
def add_card_to_deck():
  data = request.get_json()
  print('Received data', data)
  print('Json dumps: ', json.dumps(data))
  card_data = {
              'uid': settings[USER_ID],
              'image_front_url': data['image_front_url'],
              'image_front_config': json.dumps(data['image_front_config']),
              'text_front_config': json.dumps(data['text_front_config']),
              'text_front': data['text_front'],
              'image_back_url': data['image_back_url'],
              'image_back_config': json.dumps(data['image_back_config']),
              'text_back_config': json.dumps(data['text_back_config']),
              'text_back': data['text_back'],
              'right_count': 0,
              'wrong_count': 0,
              'current_level': 0,
              'next_show_date': datetime.date.today()
              }
  add_card_to_db(card_data)
  # THIS IS NOT DOING ANYTHING? MANUALLY REDIRECTING TO THIS ROUTE IN JS
  return render_template('card-added.html')

@app.route('/card-added')
@login.is_user_logged_in
def card_added_to_deck():
  return render_template('card-added.html')

# ANCHOR UPDATE CARD FROM EDIT MODE
@app.route('/update-card', methods=['POST'])
@login.is_user_logged_in
def update_card():
  data = request.get_json()
  print('Received data to update', data)
  # TODO 
  card_data = {
              'uid': settings[USER_ID],
              'card_id': data['card_id'],
              'image_front_url': data['image_front_url'],
              'image_front_config': json.dumps(data['image_front_config']),
              'text_front_config': json.dumps(data['text_front_config']),
              'text_front': data['text_front'],
              'image_back_url': data['image_back_url'],
              'image_back_config': json.dumps(data['image_back_config']),
              'text_back_config': json.dumps(data['text_back_config']),
              'text_back': data['text_back']
              }
  update_card_in_db(card_data)
  # THIS IS NOT DOING ANYTHING? MANUALLY REDIRECTING TO THIS ROUTE IN JS
  return render_template('card-added.html')

# ANCHOR CARD LIST
@app.route('/card-list')
@login.is_user_logged_in
def card_list():
  # fetch cards
  cards = fetch_all_cards_for_user(settings[USER_ID])
  return render_template('card-list.html', cards=cards, levels={0,1,2,3,4,5,6,7}, view='list')
  
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ANCHOR FILE UPLOAD HANDLE
@app.route('/upload/image', methods=['POST'])
def upload_file():
  if request.method == 'POST':
    print('we are in POST')
    print('request.method', request.method)
    print('request.args', request.args)
    print('request.form', request.form)
    print('request.files', request.files)
      # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return redirect('/error')
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print('File filename:', file.filename)
        file_ext = file.filename[-4:]
        print('File extension:', file_ext)
        new_filename = str(uuid.uuid4().hex) + file_ext
        print('New filename:', new_filename)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        return f'/static/uploads/{new_filename}', 200
  
     
