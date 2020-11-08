from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
from models import User,Bet,Event,Agreement
from app import app,db

# flask db migrate
# flask db upgrade

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

@app.route('/')
def home():
    if current_user.is_authenticated:
        bets = Bet.query.filter(Bet.id.notin_([bet.id for bet in current_user.bets_engaged_in])).filter(Bet.creator != current_user).order_by(Bet.date.desc())
        return render_template('homepage.html', user=current_user, bets=bets)   
    else: 
        bets = Bet.query.order_by(Bet.date.desc())
        return render_template('not_logged_in_homepage.html', bets=bets)

@app.route('/create_event', methods=['POST'])
def create_event():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    event_name = req['event_name']
    moderator_name = req['mod_name']
    creator_id = current_user.id
    moderator = User.query.filter_by(username=moderator_name).first()
    if event_name==None:
        return make_response(jsonify({"error":str('Invalid Event Name')}), 401) 
    elif moderator==None:
        return make_response(jsonify({"error":str('Invalid Moderator Name')}), 401) 
    else:
        moderator_id = moderator.id
        event = Event(name=event_name, creator_id=creator_id, moderator_id=moderator_id, access=True)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("eventname", variable=event_name), code=301)

@app.route('/create_bet', methods=['POST'])
def create_bet():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    if req['y_n']==None:
        return make_response(jsonify({"error":str('Pick Either Yes or No')}), 401)
    bet_amount = req['bet_amount']
    event_name = req['event_name']
    y_n = req['y_n']
    creator_id = current_user.id
    bet = Bet(creator_id=creator_id, event_name=event_name, bet_amount=bet_amount, y_n=y_n)
    db.session.add(bet)
    db.session.commit()
    return make_response(jsonify({"mod_name":str(y_n)}), 200)

@app.route('/accept', methods=['POST'])
def accept():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_id = req['bet_id']
    engagor_id = current_user.id
    creator_id = Bet.query.get(bet_id).creator_id
    print(bet_id)
    # agreement = Agreement(creator_id=creator_id, engagor_id=engagor_id, bet_id=bet_id, final=False)
    # db.session.add(agreement)
    # db.session.commit()
    return 'response'

@app.route('/agree', methods=['POST'])
def agree():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_id = req['bet_id']
    engagor_id = req['engagor_id']
    creator_id = current_user.id
    agreement = Agreement.query.filter_by(bet_id=bet_id, engagor_id=engagor_id, creator_id=creator_id).first()
    agreement.final = True
    # db.session.commit()
    return 'agree'

@app.route('/reject', methods=['POST'])
def reject():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    bet_id = req['bet_id']
    engagor_id = req['engagor_id']
    creator_id = current_user.id
    agreement = Agreement.query.filter_by(bet_id=bet_id, engagor_id=engagor_id, creator_id=creator_id).first()
    # db.session.delete(agreement)
    # db.session.commit()
    return 'reject'

@app.route('/created_bets')
def created_bets():
    bets = current_user.bets_created
    return render_template('created_bets.html', user=current_user, bets=bets)

@app.route('/bets_engaged_in')
def bets_engaged_in():
    bets_engaged_in = current_user.bets_engaged_in
    bets_created = current_user.bets_created
    events_moderated = current_user.events_moderated
    return render_template('bets_engaged_in.html', user=current_user, bets_engaged_in=bets_engaged_in, bets_created=bets_created)

@app.route('/private_bets')
def private_bets():
    return render_template('private_bets.html', user=current_user)

@app.route('/search/<variable>', methods=['GET'])
def search(variable):
    search = variable.replace(" ", " & ")
    bets = Bet.query.filter(Bet.__ts_vector__.match(search, postgresql_regconfig='english')).all()
    return render_template('search.html', user=current_user, bets=bets)

@app.route('/user/<variable>', methods=['GET'])
def user(variable):
    if variable == current_user.username:
        return render_template('user.html', user=current_user, username=variable, owner=True)
    return render_template('user.html', user=current_user, username=variable, owner=False)

@app.route('/eventname/<variable>', methods=['GET'])
def eventname(variable):
    event = Event.query.filter_by(name=variable).first()
    if event is None: return render_template('event_page.html', condition=True, user=current_user)
    bets = Bet.query.filter_by(event_name=variable).all()
    return render_template('event_page.html', user=current_user, event=event, bets=bets, condition=False)
