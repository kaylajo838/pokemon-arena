from flask import render_template, request, flash, redirect, url_for
import requests
from app import app
from .forms import PokemonNameForm, RegistrationForm, LoginForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user

@app.route('/')
def home():
    return render_template('home.html', methods=['GET'])


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit:
        new_user_dict = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        new_user = User()
        new_user.from_dict(new_user_dict)
        new_user.save_to_db()

        flash('Nice! You are officially registered!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data.lower()
        password = form.password.data

        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in! Welcome back, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user:
        logout_user()
        flash('You have been logged out, see you next time!', 'warning')
        return redirect(url_for('login'))


@app.route('/pokemon_form', methods=['GET', 'POST'])
def pokemon_form():
    form = PokemonNameForm()
    if request.method == 'POST' and form.validate_on_submit:
        name = form.pokemon_name.data.lower()
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        pokemon_response = requests.get(pokemon_url)
        if pokemon_response.ok:
            pokemon_name = pokemon_response.json()
            new_pokemon_data = []
            pokemon_dict = {
                "name": pokemon_name["forms"][0]["name"],
                "ability": pokemon_name["abilities"][0]["ability"]["name"],
                "base_experience": pokemon_name["base_experience"],
                "sprite_url": pokemon_name["sprites"]["front_shiny"],
                "attack_base_stat": pokemon_name["stats"][1]["base_stat"],
                "hp_base_stat": pokemon_name["stats"][0]["base_stat"],
                "defense_base_stat": pokemon_name["stats"][2]["base_stat"]
            }
            new_pokemon_data.append(pokemon_dict)
            return render_template('pokemon_form.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = "That pokemon doesn't exist."
            return render_template('pokemon_form.html', error=error, form=form)
    return render_template('pokemon_form.html', form=form)
