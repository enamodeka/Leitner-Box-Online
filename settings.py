from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, insert

# def init():
  # engine is created only once and can handle multiple connections
  # global engine

db_host = ''
db_name = ''
db_user = ''
db_pass = ''

with open('.config') as my_file:
	db_host = my_file.readline()
	db_name = my_file.readline()
	db_user = my_file.readline()
	db_pass = my_file.readline()

# we're using slicing here to remove new line character from the end of those strings
# also the config file has a terminating_line at the end such that no important line is without a new line character
# otherwise we would be losing character on last line
engine = create_engine(f'mysql+pymysql://{db_user[:-1]}:{db_pass[:-1]}@{db_host[:-1]}:3306/{db_name[:-1]}')
  # global logged_in_user_id
logged_in_user_id = 0

settings = []
settings.append(logged_in_user_id)
USER_ID = 0

