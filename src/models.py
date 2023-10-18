from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(db.String(120), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gravity": self.gravity,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,

        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)
    eyes_color = db.Column(db.String(120), unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='character', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "eyes_color": self.eyes_color,
            "hair_color": self.hair_color,

        }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    
    def __repr__(self):
        return '<Favorites %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }