from settings import engine, settings, USER_ID
import datetime
import arrow
import random
import json

def fetch_next_card():
  with engine.connect() as con:
    # look for cards for the user
    # if no cards return -1
    res = con.execute(f'SELECT * FROM `cards` WHERE uid IN(\'{settings[USER_ID]}\');')
    cards = []
    for row in res:
      cards.append(dict(row))
    if len(cards) == 0:
      return { 'card_id': -1 }
    else:
      # else if there are cards look if there are cards to be played today
      # if there are none return 0
      today = datetime.date.today()
      
      res = con.execute(f'SELECT * FROM `cards` WHERE uid IN(\'{settings[USER_ID]}\') AND next_show_date <= \'{today}\';')
      cards = [] # empty the cards list from the previous fetch results
      for row in res:
        cards.append(dict(row))
      # print('All cards: ', cards)
      if len(cards) == 0:
        return { 'card_id': 0 }
      else:
        # get a random card
        
        next_card = random.choice(cards)
        return {
              'card_id': next_card['card_id'], 
              'current_level': next_card['current_level'], 
              'text_front': next_card['text_front'],
              'image_front_url': next_card['image_front_url'],
              'image_front_config': json.loads(next_card['image_front_config']),
              'text_front_config': json.loads(next_card['text_front_config']),
              'text_back': next_card['text_back'],
              'image_back_url': next_card['image_back_url'],
              'image_back_config': json.loads(next_card['image_back_config']),
              'text_back_config': json.loads(next_card['text_back_config'])
              }

def fetch_card(card_id):
  with engine.connect() as con:
    res = con.execute(f'SELECT * FROM `cards` WHERE card_id IN(\'{card_id}\');')
    cards = []
    for row in res:
      cards.append(dict(row))
    if len(cards) == 0:
      return -1
    else:
      next_card = cards[0]
      return {
              'card_id': next_card['card_id'], 
              'text_front': next_card['text_front'],
              'image_front_url': next_card['image_front_url'],
              'image_front_config': json.loads(next_card['image_front_config']),
              'text_front_config': json.loads(next_card['text_front_config']),
              'text_back': next_card['text_back'],
              'image_back_url': next_card['image_back_url'],
              'image_back_config': json.loads(next_card['image_back_config']),
              'text_back_config': json.loads(next_card['text_back_config'])
              }

def fetch_all_cards_for_user(user_id):
  with engine.connect() as con:
    res = con.execute(f'SELECT * FROM `cards` WHERE uid IN(\'{settings[USER_ID]}\');')
    cards = []
    for row in res:
      cards.append(dict(row))
    if len(cards) == 0:
      return -1
    else:
      return cards

def add_card_to_db(card_data):
  with engine.connect() as con:
    res = con.execute(f'''
      INSERT INTO `cards`
      (`uid`, `image_front_url`, `image_front_config`, `text_front`, `text_front_config`, `image_back_url`, `image_back_config`, `text_back`, `text_back_config`, `right_count`, `wrong_count`, `current_level`, `next_show_date`)
      VALUES (
      \'{card_data["uid"]}\',
      \'{card_data["image_front_url"]}\',
      \'{card_data["image_front_config"]}\',
      \'{card_data["text_front"]}\',
      \'{card_data["text_front_config"]}\',
      \'{card_data["image_back_url"]}\',
      \'{card_data["image_back_config"]}\',
      \'{card_data["text_back"]}\',
      \'{card_data["text_back_config"]}\',
      \'{card_data["right_count"]}\',
      \'{card_data["wrong_count"]}\',
      \'{card_data["current_level"]}\',
      \'{card_data["next_show_date"]}\'
      );
      ''')
    # print('Insert response: ', res.is_insert)

def update_card_in_db(card_data):
  with engine.connect() as con:
    res = con.execute(f'''
      UPDATE
      `cards`
      SET
      `uid`={card_data["uid"]},
      `image_front_url`=\'{card_data["image_front_url"]}\',
      `image_front_config`=\'{card_data["image_front_config"]}\',
      `text_front`=\'{card_data["text_front"]}\',
      `text_front_config`=\'{card_data["text_front_config"]}\',
      `image_back_url`=\'{card_data["image_back_url"]}\',
      `image_back_config`=\'{card_data["image_back_config"]}\',
      `text_back`=\'{card_data["text_back"]}\',
      `text_back_config`=\'{card_data["text_back_config"]}\'
      WHERE
        `card_id`={card_data['card_id']}
      ''')
    print('Update performed')

def delete_card_in_db(card_id):
  with engine.connect() as con:
    res = con.execute(f'''
      DELETE
      FROM
      `cards`
      WHERE
      card_id = {card_id}
      ''')
    print('Card deleted')
  # .DELETE FROM `cards` WHERE card_id = 46


def count_update(card_id, answer):
  with engine.connect() as con:
    res = con.execute(f'SELECT * FROM `cards` WHERE card_id IN(\'{card_id}\');')
    cards = []
    for row in res:
      cards.append(dict(row))
    if len(cards) == 0:
      return 'Card ID error'
    card = cards[0]

    today = datetime.date.today()
    next_show_daily_increment = 0
    if answer == False:
      next_show_date = today
      current_level = 0
    else:
      if card['current_level'] == 0:
        next_show_daily_increment = 1
        current_level = 1
      else:
        next_show_daily_increment = 2**(card['current_level'])
        current_level = card['current_level'] + 1

    
    next_show_date = arrow.utcnow().shift(days=+next_show_daily_increment).date()
    print('Next show date: ', next_show_date)
    # next_show_date = datetime.date(today.year, today.month, today.day+next_show_daily_increment)

    if answer == True:
      res = con.execute(f'''
        UPDATE
        `cards`
        SET
        `current_level`={current_level},
        `right_count`={card['right_count']+1},
        `next_show_date`='{next_show_date}'
        WHERE
        `card_id`={card_id}
      ''')
    else:
      res = con.execute(f'''
        UPDATE
        `cards`
        SET
        `current_level`={current_level},
        `wrong_count`={card['wrong_count']+1},
        `next_show_date`='{today}'
        WHERE
        `card_id`={card_id}
      ''')

  return True
