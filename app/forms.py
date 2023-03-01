from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonNameForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Let\'s go!')