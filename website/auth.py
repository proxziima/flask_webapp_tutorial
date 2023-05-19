from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # Para criptografar a senha
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # Verifica se o email existe no banco de dados

        if user:
            if check_password_hash(user.password, password): 
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # Se o email e a senha estiverem corretos, loga o usuário
                return redirect(url_for('views.home')) # Se o email e a senha estiverem corretos, redireciona para a página inicial
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error') # Se o email não existir, retorna um erro
    
    return render_template("login.html.j2", user=current_user)

@auth.route('/logout')
@login_required # Só pode acessar a página se estiver logado
def logout():
    logout_user() # Desloga o usuário
    return redirect(url_for('auth.login')) # Redireciona para a página de login

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # Verifica se o email existe no banco de dados

        if user:
            flash('Email already exists.', category='error') # Se o email já existir, retorna um erro
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error') 
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) # Se o email e a senha estiverem corretos, loga o usuário
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html.j2", user=current_user)