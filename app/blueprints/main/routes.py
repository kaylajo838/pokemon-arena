from flask import render_template, request, flash, redirect, url_for
import requests
from app.blueprints.main import main
from app.blueprints.auth.forms import PokemonNameForm, CaptureForm
from flask_login import login_required, current_user
from ...models import Captured, User

@main.route('/')
@login_required
def home():
    users = User.query.all()
    return render_template('home.html', users=users)


@main.route('/pokemon_form', methods=['GET', 'POST'])
@login_required
def pokemon_form():
    form = PokemonNameForm()
    catch = CaptureForm()

    if request.method == 'POST' and form.validate_on_submit():
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

            for pokemon in current_user.captured_pokemon:
                if pokemon.name == pokemon_dict['name']:
                    flash(f'That pokemon is already on your team! Please choose another.', 'danger')
                    return redirect(url_for('main.pokemon_form'))
        
            new_pokemon_data.append(pokemon_dict)

            return render_template('pokemon_form.html', new_pokemon_data=new_pokemon_data, form=form, catch=catch)
        else:
            flash('That pokemon doesn\'t exist', 'danger')
            return redirect(url_for('main.pokemon_form'))
    return render_template('pokemon_form.html', form=form, catch=catch)


@main.route('/catch/<poke_name>')
@login_required
def catch(poke_name):
    form = PokemonNameForm()
    pokemon = Captured.query.filter_by(name=poke_name).first()
    # print(current_user.captured_pokemon.count())
    if current_user.captured_pokemon.count() >= 5:
        flash('You already have 5 pokemon on your team!', 'danger')
        return redirect(url_for('main.pokemon_form'))
    elif pokemon:
        current_user.catch(pokemon)
        flash(f'You have captured {poke_name.title()}!', 'success')
        return redirect(url_for('main.pokemon_form'))
    else:
        name = poke_name
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        pokemon_response = requests.get(pokemon_url)
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
            new_pokemon = Captured()
            new_pokemon.from_dict(pokemon_dict)
            new_pokemon.save_to_db()

            current_user.catch(new_pokemon)

            flash(f'You have captured {poke_name.title()}!', 'success')
            return redirect(url_for('main.pokemon_form'))
    return redirect(url_for('main.pokemon_form'))



# remove pokemon from team
@main.route('/remove_from_team/<name>')
@login_required
def remove_from_team(name):
    my_team = current_user.captured_pokemon
    for pokemon in my_team:
        if pokemon.name == name:
            current_user.remove_from_team(pokemon)
            flash(f'Successfully removed {pokemon.name.title()}!', 'success')
    return redirect(url_for('main.view_team'))



@main.route('/view_team')
@login_required
def view_team():
    my_team = current_user.captured_pokemon
    return render_template('view_team.html', my_team=my_team)



# ***************************DON'T TOUCH THE CODE ABOVE THIS LINE****************************************

@main.route('/battle')
@login_required
def battle():
    users = User.query.all()
    return render_template('battle_pokemon.html', users=users)
