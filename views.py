from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, make_response
from models import User,Bet,Event,Agreement
from commands import create_tables
from app import app,db

# flask db migrate
# flask db upgrade

login_manager = LoginManager()
login_manager.init_app(app)

app.cli.add_command(create_tables)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/sign_up', methods=['POST'])
def sign_up():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    username = req['username']
    password = req['password']
    user_exists = User.query.filter_by(username=username).first()
    if user_exists is not None:
        res = make_response(jsonify({"message": False}), 401)
        return res
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
    print(event_name)
    print(moderator_name)
    creator_id = current_user.id
    moderator = User.query.filter_by(username=moderator_name).first()
    event_if = Event.query.filter_by(name=event_name).first()
    if event_name=='':
        return make_response(jsonify({"error":str('Enter an Event Name')}), 401) 
    elif event_if is not None:
        return make_response(jsonify({"error":str('Event Already Exists')}), 401) 
    elif moderator==None:
        return make_response(jsonify({"error":str('Invalid Moderator Name')}), 401) 
    else:
        moderator_id = moderator.id
        event = Event(name=event_name, creator_id=creator_id, moderator_id=moderator_id, access=True)
        db.session.add(event)
        db.session.commit()
        return make_response(jsonify({"Success":"Success"}), 200)

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
    bet = Bet(creator_id=creator_id, event_name=event_name, amount = bet_amount, y_n=y_n)
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
    agreement = Agreement(creator_id=creator_id, engagor_id=engagor_id, bet_id=bet_id, final=False)
    db.session.add(agreement)
    db.session.commit()
    return 'response'

@app.route('/agree', methods=['POST'])
def agree():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    agreement_id = req['agreement_id']
    agreement = Agreement.query.filter_by(id=agreement_id).first()
    agreement.final = True
    db.session.commit()
    return 'agree'

@app.route('/reject', methods=['POST'])
def reject():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    agreement_id = req['agreement_id']
    agreement = Agreement.query.filter_by(id=agreement_id).first()
    db.session.delete(agreement)
    db.session.commit()
    return 'reject'

@app.route('/decision', methods=['POST'])
def decision():
    req = request.get_json()
    if req is None: return redirect(url_for('home'))
    event_id = req['event_id']
    decision = req['decision']
    event = Event.query.filter_by(id=event_id).first()
    agreements = event.agreements.filter(Agreement.final==False).all()
    event.decision = decision 
    if len(agreements) > 0:
        db.session.delete(agreements)
    db.session.commit()
    return make_response(jsonify({"mod_name":'last'}), 200)

@app.route('/search/<variable>', methods=['GET'])
def search(variable):
    search = variable.replace(" ", " & ")
    events = Event.query.filter(Event.__ts_vector__.match(search, postgresql_regconfig='english')).all()
    return render_template('search.html', user=current_user, events=events)

@app.route('/user/<variable>', methods=['GET'])
def user(variable):
    if variable == current_user.username:
        bets_created = current_user.bets_created
        bets_engaged_in = current_user.agreements_engaged_in.filter(Agreement.final==False).all()
        agreements_finalized = current_user.agreements_in.filter(Agreement.final==True).all()
        return render_template('user.html', user=current_user, username=variable, bets_created=bets_created, bets_engaged_in=bets_engaged_in, agreements_finalized=agreements_finalized, owner=True)
    else:
        user = User.query.filter_by(username=variable).first()
        bets_created = user.bets_created
        bets_engaged_in = user.agreements_engaged_in.filter(Agreement.final==False).all()
        agreements_finalized = user.agreements_in.filter(Agreement.final==True).all()
        return render_template('user.html', user=user, username=variable, bets_created=bets_created, bets_engaged_in=bets_engaged_in, agreements_finalized=agreements_finalized, owner=False)

@app.route('/eventname/<variable>', methods=['GET'])
def eventname(variable):
    event = Event.query.filter_by(name=variable).first()
    if event is None: return render_template('event_page.html', condition=True, user=current_user)
    bets = Bet.query.filter_by(event_name=variable).all()
    return render_template('event_page.html', user=current_user, event=event, bets=bets, condition=False)
