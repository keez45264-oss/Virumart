"""
Customer authentication: signup, login, logout.
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].strip().lower()
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db_connection()
        existing = conn.execute('SELECT * FROM users WHERE email = %s', (email,)).fetchone()

        if existing:
            conn.close()
            return render_template('auth/signup.html', error='An account with this email already exists.')

        password_hash = generate_password_hash(password)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = conn.execute(
            '''INSERT INTO users (name, email, phone, password_hash, created_at)
               VALUES (%s, %s, %s, %s, %s)
               RETURNING user_id''',
            (name, email, phone, password_hash, created_at)
        )
        user_id = cursor.fetchone()['user_id']
        conn.commit()
        conn.close()

        session['user_id'] = user_id
        session['user_name'] = name
        return redirect(url_for('customer.home'))

    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = %s', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            return redirect(url_for('customer.home'))

        return render_template('auth/login.html', error='Incorrect email or password.')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('customer.home'))