from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo

class PokemonNameForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Let\'s go!')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Login')

class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')