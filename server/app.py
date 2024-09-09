# #!/usr/bin/env python3

# from flask import Flask, request, make_response
# from flask_migrate import Migrate
# from flask_restful import Api, Resource
# from models import db, Hero, Power, HeroPower
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os
from flask import jsonify
from flask import request

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
"DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
# Route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

# Route to get one hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get_or_404(id)
    return jsonify(hero.to_dict()), 200
# Route to retrieve all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200

# Route to retrieve one power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get_or_404(id)
    return jsonify(power.to_dict()), 200

# Route to update power by ID (PATCH request)
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get_or_404(id)
    data = request.get_json()

    if 'description' in data and len(data['description']) < 20:
        return jsonify({'error': 'Description must be at least 20 characters long'}), 400

    power.description = data.get('description', power.description)
    db.session.commit()

    return jsonify(power.to_dict()), 200

# Route to create a hero_power (POST request)
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validate strength
    if data['strength'] not in ['Strong', 'Weak', 'Average']:
        return jsonify({'error': 'Strength must be Strong, Weak, or Average'}), 400

    hero_power = HeroPower(
        hero_id=data['hero_id'],
        power_id=data['power_id'],
        strength=data['strength']
    )
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict()), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)

