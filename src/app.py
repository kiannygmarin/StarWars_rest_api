"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Character, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    if len(users) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_users = list(map(lambda x: x.serialize(), users))
    return serialized_users, 200


@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all()
    if len(planets) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_planets = list(map(lambda x: x.serialize(), planets))
    return serialized_planets, 200


@app.route('/character', methods=['GET'])
def handle_character():

    character= Character.query.all()
    if len(character) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_character = list(map(lambda x: x.serialize(), character))
    return serialized_character, 200


@app.route('/favorites', methods=['GET'])
def handle_favorites():

    favorites = Favorites.query.all()
    if len(favorites) < 1:
        return jsonify({"msg": "not found"}), 404
    serialized_favorites = list(map(lambda x: x.serialize(), favorites))
    return serialized_favorites, 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": f"user with id {user_id} not found"}), 404
    serialized_user = user.serialize()
    return serialized_user, 200


@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planets(planets_id):
    planets = Planets.query.get(planets_id)
    if planets is None:
        return jsonify({"msg": f"planets with id {planets_id} not found"}), 404
    serialized_planets = planets.serialize()
    return serialized_planets, 200


@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"msg": f"character with id {character_id} not found"}), 404
    serialized_character = character.serialize()
    return serialized_character, 200


@app.route('/favorites/<int:favorites_id>', methods=['GET'])
def get_one_favorites(favorites_id):
    favorites = Favorites.query.get(favorites_id)
    if favorites is None:
        return jsonify({"msg": f"favorites with id {favorites_id} not found"}), 404
    serialized_favorites = favorites.serialize()
    return serialized_favorites, 200

@app.route('/favorites/user/<int:user_id>', methods=['DELETE'])
def delete_one_favorite_user(user_id):
    delete_favorite_user = Favorites.query.get(user_id)
    db.session.delete(delete_favorite_user)
    db.session.commit()
    return jsonify({"msg": "Favorite user deleted succesfully"}), 200


@app.route('/favorites/planet/<int:planets_id>', methods=['DELETE'])
def delete_one_favorite_planet(planets_id):
    delete_favorite_planet = Favorites.query.get(planets_id)
    db.session.delete(delete_favorite_planet)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted succesfully"}), 200

@app.route('/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_one_favorite_character(character_id):
    delete_favorite_character = Favorites.query.get(character_id)
    db.session.delete(delete_favorite_character)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted succesfully"}), 200


@app.route('/user', methods=['POST'])
def create_one_user():
    body = json.loads(request.data)
    new_user = User(
        email = body["email"],
        password = body["password"],

    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "user created succesfull"}), 200


@app.route('/planets', methods=['POST'])
def create_one_planets():
    body = json.loads(request.data)
    new_planets = Planets (
            name= body["name"],
            gravity = body["gravity"],
            population = body ["population"],
            diameter= body ["diameter"],
            rotation_period = body ["rotation_period"],

    )
    db.session.add(new_planets)
    db.session.commit()
    return jsonify({"msg": "planets created succesfull"}), 200

@app.route('/character', methods=['POST'])
def create_one_character():
    body = json.loads(request.data)
    new_character = Character (
            name= body ["name"],
            gender= body["gender"],
            height = body ["height"],
            eyes_color = body ["eyes_color"],
            hair_color= body ["hair_color"],
            

    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"msg": "character created succesfull"}), 200


@app.route('/user/<int:user_id>/favorites/planet', methods=['POST'])
def add_favorite_planet(user_id):
    body = json.loads(request.data)
    planet_id = body.get("planet_id")

    # Verificar si el planeta existe
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": f"planet with id {planet_id} not found"}), 404
   
    # Agregar el planeta como favorito
    new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites successfully"}), 200





















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


