from settings import engine, settings, USER_ID
from decorators import test_decorator
import datetime

@test_decorator
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
      print('Today', today)
      tomorrow = datetime.date(today.year, today.month, today.day+1)
      print('Tomorrow', tomorrow)
      res = con.execute(f'SELECT * FROM `cards` WHERE uid IN(\'{settings[USER_ID]}\') AND next_show_date < \'{tomorrow}\';')
      cards = [] # empty the cards list from the previous fetch results
      for row in res:
        cards.append(dict(row))
      print('All cards: ', cards)
      if len(cards) == 0:
        return { 'card_id': 0 }
      else:
        next_card = cards[0]
        return {
              'card_id': next_card['card_id'], 
              'text_front': next_card['text_front'],
              'image_front_url': next_card['image_front_url'],
              'text_back': next_card['text_back'],
              'image_back_url': next_card['image_back_url']
              }

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
    print('Insert response: ', res.is_insert)


    # res = con.execute(f'INSERT INTO `cards` (`uid`, `image_front_url`, `image_front_config`, `text_front`, `text_front_config`, `image_back_url`, `image_back_config`, `text_back`, `text_back_config`, `right_count`, `wrong_count`, `current_level`, `next_show_date`) VALUES (\'{settings[USER_ID]}\', \'{card_data["image_front_url"]}\', \'{card_data["image_front_config"]}\', \'{card_data["text_front"]}\', \'{card_data["text_front_config"]}\', \'{card_data["image_back_url"]}\', \'{card_data["image_back_config"]}\', \'{card_data["text_back"]}\', \'{card_data["text_back_config"]}\', \'{card_data["right_count"]}\', \'{card_data["wrong_count"]}\', \'{card_data["current_level"]}\', \'{card_data["next_show_date"]}\' );') 
    # print('Insert response: ', res.is_insert)    