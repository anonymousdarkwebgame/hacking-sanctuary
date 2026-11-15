import os
import random
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_NAME = "madhyamik_vault.db"

# আপনার নিজস্ব সুপার অ্যাডমিন সিড (এটি দিয়ে লগইন করলেই আপনি প্রশ্নপত্র পোস্ট করতে পারবেন)
ADMIN_SEED = "shadow-protocol-omega-zero-madhyamik-cipher-vault-17"

WORDS = [
    "cipher", "shadow", "matrix", "vortex", "phantom", "neon", "vertex", "echo",
    "zero", "omega", "apex", "delta", "pulse", "stealth", "obsidian", "onyx",
    "quantum", "rogue", "ghost", "raven", "vector", "nexus", "void", "titan"
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seed TEXT UNIQUE,
                    codename TEXT,
                    is_admin INTEGER DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author TEXT,
                    subject TEXT,
                    title TEXT,
                    content TEXT,
                    is_vault INTEGER DEFAULT 0,
                    timestamp TEXT
                )''')
    # অ্যাডমিন অ্যাকাউন্ট নিশ্চিত করা
    c.execute("INSERT OR IGNORE INTO users (seed, codename, is_admin) VALUES (?, ?, ?)",
              (ADMIN_SEED, "ARCHITECT // MENTOR 17", 1))
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MADHYAMIK SANCTUARY // 360</title>
    <style>
        body { background-color: #050505; color: #00ff41; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; }
        .container { max-width: 850px; margin: auto; border: 1px solid #00ff41; padding: 20px; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
        h1, h2, h3 { text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px dashed #00ff41; padding-bottom: 5px; }
        .vault-banner {
            display: block; background: #1a0000; border: 2px solid #ff003c; color: #ff003c;
            text-align: center; padding: 15px; font-weight: bold; font-size: 1.1em;
            text-decoration: none; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px;
            box-shadow: 0 0 12px rgba(255, 0, 60, 0.4);
        }
        .vault-banner:hover { background: #ff003c; color: #000; }
        .nav { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
        .nav a { color: #00ff41; text-decoration: none; border: 1px solid #00ff41; padding: 6px 12px; font-size: 0.9em; }
        .nav a:hover { background: #00ff41; color: #000; }
        input, textarea, select {
            width: 100%; background: #0d0d0d; border: 1px solid #00ff41; color: #00ff41;
            padding: 10px; margin: 8px 0; font-family: inherit; box-sizing: border-box;
        }
        button {
            background: #00ff41; color: #000; border: none; padding: 10px 20px;
            font-weight: bold; cursor: pointer; font-family: inherit; text-transform: uppercase;
        }
        button:hover { background: #00cc33; }
        .post { border: 1px solid #004d13; background: #0a0a0a; padding: 15px; margin-bottom: 15px; }
        .vault-post { border: 1px solid #ff003c; background: #120004; }
        .vault-post h3 { color: #ff003c; border-bottom-color: #ff003c; }
        .meta { font-size: 0.8em; color: #888; margin-bottom: 8px; }
        .seed-box { background: #111; border: 1px dashed #ffcc00; color: #ffcc00; padding: 12px; margin: 10px 0; word-break: break-all; }
    </style>
</head>
<body>
<div class="container">
    <h1>[ THE SANCTUARY // MADHYAMIK ]</h1>
    
    <a href="{{ url_for('vault') }}" class="vault-banner">
        [!] WHERE QUESTION PAPERS FOR MADHYAMIK ARE PREPARED [!]
    </a>

    <div class="nav">
        <a href="{{ url_for('index') }}">STUDENT BLOG</a>
        <a href="{{ url_for('vault') }}" style="border-color:#ff003c; color:#ff003c;">FINAL SUGGESTIONS</a>
        {% if session.get('user') %}
            <a href="{{ url_for('create_post') }}">+ NEW POST</a>
            <a href="{{ url_for('logout') }}">LOGOUT ({{ session['codename'] }})</a>
        {% else %}
            <a href="{{ url_for('login') }}">ACCESS / GENERATE ID</a>
        {% endif %}
    </div>

    {% if page == 'login' %}
        <h2>IDENTITY AUTHENTICATION</h2>
        {% if new_seed %}
            <div class="seed-box">
                <strong>YOUR NEW 8-WORD RECOVERY SEED (SAVE THIS!):</strong><br><br>
                {{ new_seed }}
            </div>
        {% endif %}
        <form method="POST">
            <label>ENTER YOUR 8-WORD SEED:</label>
            <input type="text" name="seed" placeholder="word1-word2-word3-word4-word5-word6-word7-word8" required>
            <button type="submit">ENTER SANCTUARY</button>
        </form>
        <br>
        <form method="POST" action="{{ url_for('generate_id') }}">
            <button type="submit" style="background:#ffcc00;">GENERATE NEW ANONYMOUS IDENTITY</button>
        </form>

    {% elif page == 'create' %}
        <h2>TRANSMIT NEW ENTRY</h2>
        <form method="POST">
            <label>SUBJECT:</label>
            <select name="subject">
                <option value="BENGALI">BENGALI (বাংলা)</option>
                <option value="ENGLISH">ENGLISH</option>
                <option value="MATHEMATICS">MATHEMATICS (গণিত)</option>
                <option value="PHYSICAL SCIENCE">PHYSICAL SCIENCE (ভৌতবিজ্ঞান)</option>
                <option value="LIFE SCIENCE">LIFE SCIENCE (জীবনবিজ্ঞান)</option>
                <option value="HISTORY">HISTORY (ইতিহাস)</option>
                <option value="GEOGRAPHY">GEOGRAPHY (ভূগোল)</option>
            </select>
            <label>TITLE:</label>
            <input type="text" name="title" placeholder="Chapter / Topic Name..." required>
            <label>CONTENT / QUESTIONS:</label>
            <textarea name="content" rows="8" placeholder="Write notes or questions here..." required></textarea>
            
            {% if session.get('is_admin') == 1 %}
                <label style="color:#ff003c;">
                    <input type="checkbox" name="is_vault" value="1" style="width:auto;"> 
                    PUBLISH TO [WHERE QUESTION PAPERS ARE PREPARED] VAULT
                </label><br><br>
            {% endif %}
            <button type="submit">PUBLISH TO NETWORK</button>
        </form>

    {% else %}
        <h2>{{ heading }}</h2>
        {% if not posts %}
            <p style="color:#666;">NO TRANSMISSIONS RECORDED YET.</p>
        {% endif %}
        {% for p in posts %}
            <div class="post {% if p[5] == 1 %}vault-post{% endif %}">
                <div class="meta">[{{ p[2] }}] // BY: {{ p[1] }} // {{ p[6] }}</div>
                <h3>{{ p[3] }}</h3>
                <p style="white-space: pre-wrap;">{{ p[4] }}</p>
            </div>
        {% endfor %}
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    posts = conn.execute("SELECT * FROM posts WHERE is_vault = 0 ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, page='feed', heading='STUDENT DISCUSSION & NOTES', posts=posts)

@app.route('/vault')
def vault():
    conn = sqlite3.connect(DB_NAME)
    posts = conn.execute("SELECT * FROM posts WHERE is_vault = 1 ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, page='feed', heading='CLASSIFIED: FINAL MADHYAMIK SUGGESTIONS', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        seed = request.form.get('seed').strip()
        conn = sqlite3.connect(DB_NAME)
        user = conn.execute("SELECT * FROM users WHERE seed = ?", (seed,)).fetchone()
        conn.close()
        if user:
            session['user'] = user[1]
            session['codename'] = user[2]
            session['is_admin'] = user[3]
            return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, page='login')

@app.route('/generate', methods=['POST'])
def generate_id():
    new_seed = "-".join(random.sample(WORDS, 8))
    codename = f"OPERATIVE-{random.randint(100, 999)}"
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO users (seed, codename, is_admin) VALUES (?, ?, 0)", (new_seed, codename))
    conn.commit()
    conn.close()
    return render_template_string(HTML_TEMPLATE, page='login', new_seed=new_seed)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if not session.get('user'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form.get('subject')
        title = request.form.get('title')
        content = request.form.get('content')
        is_vault = 1 if (request.form.get('is_vault') == '1' and session.get('is_admin') == 1) else 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO posts (author, subject, title, content, is_vault, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                     (session['codename'], subject, title, content, is_vault, now))
        conn.commit()
        conn.close()
        return redirect(url_for('vault' if is_vault == 1 else 'index'))
    return render_template_string(HTML_TEMPLATE, page='create')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
