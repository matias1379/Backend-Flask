from flask import render_template, redirect, flash, url_for, session
from flask_login import login_user, login_required, logout_user
from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': LoginForm()
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido otra vez')

                redirect(url_for('hello'))

        flash('Nombre de usario registrado con éxito!')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))
