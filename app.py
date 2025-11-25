from flask import Flask, render_template, redirect, url_for, flash, request, session
from config import Config
from models import db, User
from forms import RegisterForm, LoginForm
from quiz_data import get_random_question
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# init extensions
db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

with app.app_context():
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    db.create_all()

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#weather 3-day aggregator
def get_3day_weather(city, api_key):
    if not api_key:
        return None
    
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    try:
        r = requests.get(url, params=params, timeout=6)
        r.raise_for_status()
    except Exception:
        return None
    
    data = r.json()
    today = datetime.date.today()
    results = []

    # for today, tomorrow, day after
    for i in range(3):
        day = today + datetime.timedelta(days=i)
        day_entries = [
            item for item in data.get('list', []) 
            if datetime.datetime.fromtimestamp(item['dt']).date() == day
        ]
        day_name = day.strftime('%A')
        if not day_entries:
            results.append({
                'date': day.isoformat(), 
                'day_name': day_name, 
                'day_temp': None, 
                'night_temp': None
            })
            continue

        day_temps = [
            e['main']['temp'] 
            for e in day_entries 
            if 6 <= datetime.datetime.fromtimestamp(e['dt']).hour <= 18
        ]
        night_temps = [
            e['main']['temp'] 
            for e in day_entries 
            if not (6 <= datetime.datetime.fromtimestamp(e['dt']).hour <= 18)
        ]
        day_avg = round(sum(day_temps)/len(day_temps),1) if day_temps else None
        night_avg = round(sum(night_temps)/len(night_temps),1) if night_temps else None
        results.append({
            'date': day.isoformat(), 
            'day_name': day_name, 
            'day_temp': day_avg, 
            'night_temp': night_avg
        })

    return results

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    forecast = None
    city = ''
    if request.method == 'POST':
        city = request.form.get('city','').strip()
        if city:
            forecast = get_3day_weather(city, app.config.get('WEATHER_API_KEY'))
            if forecast is None:
                flash('Gagal mengambil data cuaca. Periksa nama kota atau API key.')
    return render_template('index.html', forecast=forecast, city=city)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username sudah dipakai. Pilih username lain.')
        elif User.query.filter_by(nickname=form.nickname.data).first():
            flash('Nickname sudah dipakai. Pilih nickname lain.')
        else:
            u = User(username=form.username.data, nickname=form.nickname.data)
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash('Registrasi sukses. Silakan login.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            flash('Login berhasil.')
            return redirect(url_for('index'))
        flash('Login gagal. Periksa username/password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Quiz route
@app.route('/quiz', methods=['GET','POST'])
@login_required
def quiz():
    if 'quiz_temp_score' not in session:
        session['quiz_temp_score'] = 0
    if 'current_q' not in session:
        q = get_random_question()
        session['current_q'] = q['q']
        session['current_options'] = q['options']
        session['current_q_a'] = q['a']

    if request.method == 'POST':
        chosen = request.form.get('choice')
        try:
            chosen_i = int(chosen)
        except Exception:
            chosen_i = -1
        correct = int(session.get('current_q_a', -1))
        if chosen_i == correct:
            session['quiz_temp_score'] = session.get('quiz_temp_score', 0) + 1

        # prepare next question
        q = get_random_question()
        session['current_q'] = q['q']
        session['current_options'] = q['options']
        session['current_q_a'] = q['a']
        return redirect(url_for('quiz'))

    # show current question
    return render_template(
        'quiz.html',
        question=session.get('current_q'),
        options=session.get('current_options', []),
        temp_score=session.get('quiz_temp_score', 0),
        total_score=current_user.total_score
    )


# finish quiz
@app.route('/quiz/finish', methods=['POST'])
@login_required
def quiz_finish():
    temp = session.get('quiz_temp_score', 0)
    if temp > 0:
        user = User.query.get(current_user.id)
        user.total_score = (user.total_score or 0) + temp
        db.session.commit()
    session.pop('quiz_temp_score', None)
    session.pop('current_q', None)
    session.pop('current_options', None)
    session.pop('current_q_a', None)
    flash(f'Quiz selesai. {temp} poin ditambahkan ke total skor Anda.')
    return redirect(url_for('leaderboard'))


@app.route('/leaderboard')
def leaderboard():
    top = User.query.order_by(User.total_score.desc()).limit(50).all()
    return render_template('leaderboard.html', top=top)


if __name__ == '__main__':
    app.run(debug=True)