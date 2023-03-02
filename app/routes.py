from flask import render_template, request
import requests
from app import app
from .forms import PokemonNameForm
from .forms import RegistrationForm
from .forms import LoginForm

@app.route('/')
def home():
    return render_template('home.html', methods=['GET'])

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

@app.route('/registration', methods=['GET', 'POST'])
def registration():

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')