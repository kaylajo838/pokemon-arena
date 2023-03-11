from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


team = db.Table('team',
        db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('captured_pokemon_id', db.Integer, db.ForeignKey('captured.id'))
        )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    captured_pokemon = db.relationship('Captured', secondary = team, backref='owner', lazy='dynamic')
    
    # hash password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    # checks hashed password
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # register user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    def update_from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']

    # save to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # catch method
    def catch(self, poke):
        self.captured_pokemon.append(poke)
        db.session.commit()

    # remove from team method
    def remove_from_team(self, user):
        self.captured_pokemon.remove(user)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Captured(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    sprite_url = db.Column(db.String)
    attack_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)

    # register captured attributes
    def from_dict(self, data):
        self.name = data['name']
        self.ability = data['ability']
        self.base_experience = data['base_experience']
        self.sprite_url = data['sprite_url']
        self.attack_base_stat = data['attack_base_stat']
        self.hp_base_stat = data['hp_base_stat']
        self.defense_base_stat = data['defense_base_stat']

    # Save the capture to database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Update our db
    def update_to_db(self):
        db.session.commit()

    # Delete from db
    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()


