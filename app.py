# app.py
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# Cyberpunk theme CSS
CYBERPUNK_STYLE = """
<style>
    /* Import Rajdhani font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');

    body {
        background-color: #1a1a1a;
        color: #ffeb3b;
        font-family: 'Rajdhani', sans-serif;
        margin: 0;
        padding: 20px;
        font-size: 28px; /* Base font size */
    }
    .nav {
        background-color: #2d1b3e;
        padding: 15px;
        margin-bottom: 20px;
    }
    .nav a {
        color: #ff00ff;
        text-decoration: none;
        margin-right: 25px;
        font-weight: 600;
        font-size: 32px;
    }
    .nav a:hover {
        color: #ffeb3b;
    }
    .content {
        background-color: #2d1b3e;
        padding: 25px;
        border: 2px solid #ff00ff;
    }
    h1 {
        font-size: 46px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    h2 {
        font-size: 40px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    p {
        font-size: 30px;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    input {
        background-color: #2d1b3e;
        border: 1px solid #ff00ff;
        color: #ffeb3b;
        padding: 8px 12px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: 28px;
    }
    button {
        background-color: #ff00ff;
        color: #1a1a1a;
        border: none;
        padding: 8px 20px;
        cursor: pointer;
        font-family: 'Rajdhani', sans-serif;
        font-size: 28px;
        font-weight: 600;
    }
    button:hover {
        background-color: #ff33ff;
    }
</style>
"""


def read_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


def get_game_stage():
    try:
        with open('status.txt', 'r') as file:
            return int(file.readline().strip())
    except (FileNotFoundError, ValueError):
        return 1


@app.route('/')
def home():
    content = read_file_content('pages/home.txt')
    return render_template_string(CYBERPUNK_STYLE + content)


@app.route('/news')
def news():
    content = read_file_content('pages/news.txt')
    return render_template_string(CYBERPUNK_STYLE + content)


@app.route('/faq')
def faq():
    content = read_file_content('pages/faq.txt')
    return render_template_string(CYBERPUNK_STYLE + content)


@app.route('/page1')
def page1():
    content = read_file_content('pages/page1.txt')
    return render_template_string(CYBERPUNK_STYLE + content)


@app.route('/page2')
def page2():
    content = read_file_content('pages/page2.txt')
    return render_template_string(CYBERPUNK_STYLE + content)


@app.route('/character')
def character():
    char_name = request.args.get('name')
    if not char_name:
        return "Character name not provided", 400

    char_file = f'characters/{char_name}.txt'
    if not os.path.exists(char_file):
        return "Character not found", 404

    # Show password form
    return render_template_string(CYBERPUNK_STYLE + """
        <div class="content">
            <h2>Enter Password</h2>
            <form action="/verify_character" method="POST">
                <input type="hidden" name="char_name" value="{{ char_name }}">
                <input type="password" name="password" required>
                <button type="submit">Submit</button>
            </form>
        </div>
    """, char_name=char_name)


@app.route('/verify_character', methods=['POST'])
def verify_character():
    char_name = request.form.get('char_name')
    password = request.form.get('password')

    if not char_name or not password:
        return "Invalid request", 400

    # Get current game stage
    current_stage = get_game_stage()

    # Read character file
    char_file = f'characters/{char_name}.txt'
    try:
        with open(char_file, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{password}, {current_stage}"):
                    content_file = lines[i + 1].strip()
                    content = read_file_content(f'content/{content_file}')
                    if content:
                        return render_template_string(CYBERPUNK_STYLE + content)
                    break
    except FileNotFoundError:
        pass

    return "Invalid password or stage", 403


if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('pages', exist_ok=True)
    os.makedirs('characters', exist_ok=True)
    os.makedirs('content', exist_ok=True)
    app.run(host='0.0.0.0', port=80)
