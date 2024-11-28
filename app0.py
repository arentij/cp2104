from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
import json
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration
CONTENT_DIR = 'content'
CHARACTERS_DIR = os.path.join(CONTENT_DIR, 'characters')
NEWS_DIR = os.path.join(CONTENT_DIR, 'news')
GAME_STATE_FILE = os.path.join(CONTENT_DIR, 'game_state.json')
CODES_FILE = os.path.join(CONTENT_DIR, 'codes.json')

# Ensure required directories exist
for directory in [CONTENT_DIR, CHARACTERS_DIR, NEWS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Initialize game state if it doesn't exist
if not os.path.exists(GAME_STATE_FILE):
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump({'current_phase': 1}, f)


def load_game_state():
    with open(GAME_STATE_FILE, 'r') as f:
        return json.load(f)


def save_game_state(state):
    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(state, f)


def load_character_codes():
    if os.path.exists(CODES_FILE):
        with open(CODES_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_character_codes(codes):
    with open(CODES_FILE, 'w') as f:
        json.dump(codes, f)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    return decorated_function


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/news')
def news():
    game_state = load_game_state()
    current_phase = game_state['current_phase']
    news_items = []

    # Load news for current and previous phases
    for phase in range(1, current_phase + 1):
        news_file = os.path.join(NEWS_DIR, f'phase_{phase}.txt')
        if os.path.exists(news_file):
            with open(news_file, 'r', encoding='utf-8') as f:
                news_items.extend(f.readlines())

    return render_template('news.html', news_items=news_items)


@app.route('/characters')
def characters():
    characters = []
    for char_file in os.listdir(CHARACTERS_DIR):
        if char_file.endswith('.json'):
            char_name = char_file[:-5]  # Remove .json extension
            characters.append({
                'name': char_name,
                'url': url_for('character', name=char_name)
            })
    return render_template('characters.html', characters=characters)


@app.route('/character/<name>', methods=['GET', 'POST'])
def character(name):
    game_state = load_game_state()
    current_phase = game_state['current_phase']
    char_file = os.path.join(CHARACTERS_DIR, f'{name}.json')
    codes = load_character_codes()

    if not os.path.exists(char_file):
        return "Character not found", 404

    with open(char_file, 'r', encoding='utf-8') as f:
        character_data = json.load(f)

    if request.method == 'POST':
        entered_code = request.form.get('code')
        char_codes = codes.get(name, {})

        if entered_code in char_codes:
            content_phase = char_codes[entered_code]
            if content_phase <= current_phase:
                return render_template('character_content.html',
                                       name=name,
                                       content=character_data[f'phase_{content_phase}'],
                                       image=character_data.get('image'))
            else:
                flash("This content is not available yet.")
        else:
            flash("Invalid code")

    return render_template('character_code.html', name=name)


@app.route('/faq')
def faq():
    faq_file = os.path.join(CONTENT_DIR, 'faq.txt')
    if os.path.exists(faq_file):
        with open(faq_file, 'r', encoding='utf-8') as f:
            faq_content = f.read()
    else:
        faq_content = "FAQ content coming soon..."
    return render_template('faq.html', content=faq_content)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(generate_password_hash('your-admin-password'), password):  # Change this password
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        flash('Invalid password')
    return render_template('admin_login.html')


@app.route('/admin/panel', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    if request.method == 'POST':
        game_state = load_game_state()
        game_state['current_phase'] = int(request.form.get('phase', 1))
        save_game_state(game_state)
        flash('Game phase updated successfully')

    game_state = load_game_state()
    return render_template('admin_panel.html', current_phase=game_state['current_phase'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)