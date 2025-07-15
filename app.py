# scibot.py

from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import google.generativeai as genai
import markdown2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import uuid

# --- Configuration ---
app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Extensions ---
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    uploader_name = db.Column(db.String(100))
    course = db.Column(db.String(100))

class ChatMemory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    context_text = db.Column(db.Text)

# --- User Loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Utils ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

# --- Routes ---
@app.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    name = request.form.get('name')
    course = request.form.get('course')

    if not file or file.filename == '':
        flash('No file selected.')
        return redirect(url_for('index'))

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_q = Question(filename=filename, uploader_name=name, course=course)
        db.session.add(new_q)
        db.session.commit()

        flash('Upload successful.')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    answer = ""
    questions = Question.query.all()
    session_id = session['session_id']

    memory = ChatMemory.query.filter_by(session_id=session_id).first()
    if not memory:
        memory = ChatMemory(session_id=session_id, context_text="")
        db.session.add(memory)
        db.session.commit()

    chat_history_html = ""
    context_lines = memory.context_text.strip().splitlines()
    for line in context_lines:
        if line.startswith("User:"):
            chat_history_html += f'<p><strong>You:</strong> {line[5:].strip()}</p>'
        elif line.startswith("AI:"):
            chat_history_html += f'<p><strong>AI:</strong> {line[3:].strip()}</p>'

    if request.method == 'POST':
        user_input = request.form['question']
        selected_files = request.form.getlist('selected_files')
        use_ocr = request.form.get('use_ocr', 'off') == 'on'

        combined_text = ""
        for filename in selected_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            text = ""

            try:
                if filename.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                elif filename.endswith('.pdf'):
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text

                    if not text.strip() and use_ocr:
                        images = convert_from_path(file_path)
                        for img in images:
                            text += pytesseract.image_to_string(img)
                else:
                    text = "[Unsupported file format]"
            except Exception as e:
                text = f"[Error reading {filename}: {e}]"

            combined_text += f"\n\n--- {filename} ---\n{text}\n"

        if combined_text:
            memory.context_text += combined_text

        memory.context_text += f"\n\nUser: {user_input}\n"

        genai.configure(api_key="") #INSERT your API KEY HERE
        model = genai.GenerativeModel("gemini-2.0-flash-exp")

        try:
            prompt = memory.context_text + "\nAI:"
            response = model.generate_content(prompt)
            model_response = response.text.strip()
            answer = markdown2.markdown(model_response)

            memory.context_text += f"AI: {model_response}\n"

            chat_history_html += f'<p><strong>You:</strong> {user_input}</p>'
            chat_history_html += f'<p><strong>AI:</strong> {model_response}</p>'

        except Exception as e:
            answer = f"<p>\u26a0\ufe0f Gemini API Error: {str(e)}</p>"

        db.session.commit()

    return render_template('chat.html', answer=answer, questions=questions, chat_history=chat_history_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
