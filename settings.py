from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, insert

# def init():
  # engine is created only once and can handle multiple connections
  # global engine
engine = create_engine('mysql+pymysql://leitnerbox:leitnerbox@localhost:3306/leitnerbox')
  # global logged_in_user_id
logged_in_user_id = 0

settings = []
settings.append(logged_in_user_id)
USER_ID = 0