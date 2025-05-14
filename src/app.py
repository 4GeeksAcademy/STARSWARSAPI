"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Planeta,People,Favoritos
from sqlalchemy import select
from werkzeug.security import generate_password_hash
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/users", methods=["GET"])
def get_users():
    stmt = select(User) 
    users = db.session.execute(stmt).scalars().all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/users", methods=["POST"])
def create_user():
   
    #if request.content_type != "application/json":
     #if not request.is_json:
        #return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.get_json()

 

    #if not data or "email" not in data or "password" not in data:
     #   return jsonify({"error": "Missing data"}), 400

    new_user = User(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        username = data["username"],
        lastname = data["lastname"],
        is_active = True

                )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    stmt = select(User).where(User.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
   
    return jsonify(user.serialize()), 200

@app.route("/planets", methods=["GET"])
def get_planets():
    stmt = select(Planeta) 
    planets = db.session.execute(stmt).scalars().all()
    
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route("/planets/<int:planeta_id>", methods=["GET"])
def get_planeta(planeta_id):
    stmt = select(Planeta).where(Planeta.id == planeta_id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "User not found"}), 404
   
    return jsonify(planet.serialize()), 200

@app.route("/Peoples", methods=["GET"])
def get_peoples():
    stmt = select(People) 
    peoples = db.session.execute(stmt).scalars().all()
    
    return jsonify([people.serialize() for people in peoples]), 200

@app.route("/Peoples/<int:people_id>", methods=["GET"])
def get_people(people_id):
    stmt = select(People).where(People.id == people_id)
    people = db.session.execute(stmt).scalar_one_or_none()
    if people is None:
        return jsonify({"error": "User not found"}), 404
   
    return jsonify(people.serialize()), 200



@app.route("/Favoritos", methods=["GET"])
def get_enrollments():
    favoritos = db.session.execute(select(Favoritos)).scalars().all()
    return jsonify([e.serialize() for e in favoritos]), 200

@app.route("/Favoritos", methods=["POST"])
def create_enrollment():
    data = request.get_json()
    new_favorito = Favoritos(
        user_id=data["user_id"],
        people_id=data["people_id"],
        planeta_id=data["planeta_id"]
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify(new_favorito.serialize()), 201

@app.route("/Favoritos/planeta/<int:planeta_id>", methods=["POST"])
def create_planeta_favorito(planeta_id):
    data = request.get_json()
    new_favorito = Favoritos(
        user_id=data["user_id"],
        #people_id=data["people_id"],
        planeta_id=planeta_id
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify(new_favorito.serialize()), 201
@app.route("/Favoritos/people/<int:people_id>", methods=["POST"])
def create_people_favorito(people_id):
    data = request.get_json()
    new_favorito = Favoritos(
        user_id=data["user_id"],
        people_id=people_id,
        #planeta_id=planeta_id
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify(new_favorito.serialize()), 201

@app.route("/Favoritos/planeta/<int:planeta_id>", methods=["DELETE"])
def delete_planeta(planeta_id):
    stmt = select(Favoritos).where(Favoritos.planeta_id == planeta_id)
    planeta = db.session.execute(stmt).scalar_one_or_none()
    if planeta is None:
        return jsonify({"error": "planeta not found"}), 404

    db.session.delete(planeta)
    db.session.commit()
    return jsonify({"message": "planeta deleted"}), 200

@app.route("/Favoritos/pepople/<int:people_id>", methods=["DELETE"])
def delete_people(people_id):
    stmt = select(Favoritos).where(Favoritos.people_id == people_id)
    people = db.session.execute(stmt).scalar_one_or_none()
    if people is None:
        return jsonify({"error": "people not found"}), 404

    db.session.delete(people)
    db.session.commit()
    return jsonify({"message": "people deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
