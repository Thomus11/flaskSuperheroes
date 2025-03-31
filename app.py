from flask import Flask ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from models import Hero,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)
migrate = Migrate(app, db)

from models import Hero,Power,HeroPower

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify({
        **hero.to_dict(),
        "hero_powers": [hp.to_dict() for hp in hero.hero_powers]
    }), 200

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if 'description' not in data:
        return jsonify({"errors": ["description is required"]}), 400

    try:
        power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict()), 200
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": ["An error occurred"]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    hero = Hero.query.get(data.get('hero_id'))
    if not hero:
        return jsonify({"errors": ["Hero not found"]}), 404

    power = Power.query.get(data.get('power_id'))
    if not power:
        return jsonify({"errors": ["Power not found"]}), 404

    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except KeyError:
        return jsonify({"errors": ["Invalid data"]}), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug = True)

