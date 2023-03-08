from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.main import main
from app.blueprints.auth.forms import PokemonNameForm
from flask_login import login_required
from ...models import Captured

@main.route('/')
@login_required
def home():
    return render_template('home.html', methods=['GET'])


@main.route('/pokemon_form', methods=['GET', 'POST'])
@login_required
def pokemon_form():
    form = PokemonNameForm()
    captured_pokemon = Captured.query.all()
    if request.method == 'POST' and form.validate_on_submit() and Captured.query.count() < 5:
        name = form.pokemon_name.data.lower()
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        pokemon_response = requests.get(pokemon_url)
        pokemon_data = []
        if pokemon_response.ok:
            pokemon_name = pokemon_response.json()
            pokemon_dict = {
                "name": pokemon_name["forms"][0]["name"],
                "ability": pokemon_name["abilities"][0]["ability"]["name"],
                "base_experience": pokemon_name["base_experience"],
                "sprite_url": pokemon_name["sprites"]["front_shiny"],
                "attack_base_stat": pokemon_name["stats"][1]["base_stat"],
                "hp_base_stat": pokemon_name["stats"][0]["base_stat"],
                "defense_base_stat": pokemon_name["stats"][2]["base_stat"]
            }

            poke_name = Captured.query.filter_by(name=pokemon_dict['name']).first()
            if poke_name:
                flash(f'That pokemon is already on your team! Please choose another.', 'danger')
                return redirect(url_for('main.pokemon_form'))
        
            pokemon_data.append(pokemon_dict)

            new_pokemon = Captured()

            new_pokemon.from_dict(pokemon_dict)

            new_pokemon.save_to_db()

            return redirect(url_for('main.pokemon_form'))
         
        else:
            flash('That pokemon doesn\'t exist', 'danger')
            return redirect(url_for('main.pokemon_form'))
    elif request.method == 'POST' and form.validate_on_submit() and Captured.query.count() >= 5:
        flash('You already have 5 Pokemon on your team!', 'danger')
        return render_template('pokemon_form.html', form=form, captured_pokemon=captured_pokemon)
    return render_template('pokemon_form.html', form=form, captured_pokemon=captured_pokemon)


