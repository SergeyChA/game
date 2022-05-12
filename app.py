import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yg645fre3uyt64gc6r65fre5tc6e4e65rt6c'
db = SQLAlchemy(app)
# login_manager = LoginManager(app)


def game_row(level):
    td = ''
    column = [td for i in range(level ** 2)]
    ind = [*random.sample(range(0, level ** 2 - 1), level)]
    for en in range(len(column)-1):
        if en in ind:
            column[en] = 'image'
    return column


def game_field(level):
    lst = game_row(level)
    field = []
    for i in range(0, len(lst), level):
        field.append(lst[i:i + level])
    return field








