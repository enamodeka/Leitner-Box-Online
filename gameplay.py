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