from flask import render_template, request, flash, redirect, url_for, session, abort
from app import app, game_field, db
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
import re


@app.route('/', methods=['POST', 'GET'])
def game():
    if session.get('level'):
        if request.method == 'POST':
            session['level'] = session.get('level') + 1
            return render_template('game.html', field=game_field(session.get('level')), level=session.get('level'))
        if session.get('level') + 1 > 5:
            return render_template('login.html')
    else:
        session['level'] = 2
    return render_template('game.html', field=game_field(session.get('level')), level=session.get('level'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Users.query.filter(Users.email == request.form['email']).first()
        if user and check_password_hash(user.password, request.form['pass']):
            session['email'] = request.form['email']
            return redirect(url_for('profile', email=request.form['email']))# нужен ли профиль
        else:
            flash('Неправильный email или пароль', category='error')
    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if not Users.query.filter(Users.email == request.form['email']).first():
            pattern = r'^((([0-9A-Za-z]{1}[-0-9A-z\.]{0,30}[0-9A-Za-z]?)|([0-9А-Яа-я]{1}[-0-9А-я\.]' \
                      r'{0,30}[0-9А-Яа-я]?))@([-A-Za-z]{1,}\.){1,}[-A-Za-z]{2,})$'
            if re.fullmatch(pattern, request.form['email']):
                hash_pass = generate_password_hash(request.form['pass'])
                user = Users(request.form['email'], hash_pass)
                db.session.add(user)
                db.session.commit()
                flash('Вы зарегистрированы', category='success')
                return redirect(url_for('login'))
            else:
                flash('Неправильный email', category='error')
        else:
            flash('Такой email уже зарегистрирован', category='error')
    return render_template('registration.html')


@app.route('/profile/<email>', methods=['POST', 'GET'])
def profile(email):
    if 'email' not in session or session['email'] != email:
        abort(401)
    user = Users.query.filter(Users.email == session.get('email')).first()
    if request.method == 'POST':
        user.level += 1
        db.session.add(user)
        db.session.commit()
        return render_template('profile.html', field=game_field(user.level), level=user.level, email=email)
    return render_template('profile.html', field=game_field(user.level), level=user.level, email=email)



@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html'), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
