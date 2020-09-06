from app import app,db
from models import User,Bet,Event,Agreement
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response

# cd Github/bet.net/
# python
# from models import db
# db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/sign_up', methods=['POST'])
def sign_up():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    username = req['username']
    password = req['password']
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('home'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    username = req['username']
    password = req['password']
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        flash('Invalid username or password')
        res = make_response(jsonify({"message": False}), 200)
        return res
    login_user(user)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/')
def home():
    if current_user.is_authenticated:
        bets = Bet.query.filter(Bet.id.notin_([bet.id for bet in current_user.bets_engaged_in])).filter(Bet.creator != current_user).order_by(Bet.date.desc())
        return render_template('homepage.html', user=current_user, bets=bets)
    else: 
        bets = Bet.query.order_by(Bet.date.desc())
        return render_template('not_logged_in_homepage.html', bets=bets)

@app.route('/create', methods=['POST'])
def create():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_amount = req['bet_amount']
    event_name = req['event_name']
    creator_id = current_user.id
    bet = Bet(creator_id=creator_id, event_name=event_name, bet_amount=bet_amount, access=True)
    db.session.add(bet)
    db.session.commit()
    return 'response'

@app.route('/accept', methods=['POST'])
def accept():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_id = req['bet_id']
    engagor_id = current_user.id
    creator_id = Bet.query.get(bet_id).creator_id
    agreement = Agreement(creator_id=creator_id, engagor_id=engagor_id, bet_id=bet_id, final=False)
    db.session.add(agreement)
    db.session.commit()
    return 'response'

@app.route('/agree', methods=['POST'])
def agree():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_id = req['bet_id']
#     admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
    db.session.commit()
    return 'agree'

@app.route('/created_bets')
def created_bets():
    bets = current_user.bets
    return render_template('created_bets.html', bets=bets)

@app.route('/bets_engaged_in')
def bets_engaged_in():
    bets = current_user.bets_engaged_in
    return render_template('bets_engaged_in.html', bets=bets)

@app.route('/private_bets')
def private_bets():
    return render_template('private_bets.html')

@app.route('/search', methods=['POST'])
def search():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    search = req['search']
    search = search.replace(" ", " & ")
    print(search)
    bets = Bet.query.filter(Bet.__ts_vector__.match(search, postgresql_regconfig='english')).all()
    print(bets)
    return str(bets)
