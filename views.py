from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import functools

views = Blueprint('views', __name__)

# In-memory user and notes storage (for demo only)
USERS = {'test': 'password'}  # username: password
NOTES = {}  # username: [list of notes]

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('views.login'))
        return view(**kwargs)
    return wrapped_view

@views.route('/', methods=['GET'])
@login_required
def home():
    username = session['username']
    user_notes = NOTES.get(username, [])
    return render_template('index.html', notes=user_notes, username=username)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            NOTES.setdefault(username, [])
            return redirect(url_for('views.home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@views.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('views.login'))

@views.route('/add_note', methods=['POST'])
@login_required
def add_note():
    note = request.form['note']
    username = session['username']
    if note:
        NOTES.setdefault(username, []).append(note)
    return redirect(url_for('views.home'))

@views.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    username = session['username']
    user_notes = NOTES.get(username, [])
    if 0 <= note_id < len(user_notes):
        user_notes.pop(note_id)
    return redirect(url_for('views.home'))