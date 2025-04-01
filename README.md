This project is a Flask-based RESTful API that manages data about heroes, powers, and their relationships. 
It allows users to perform CRUD operations on heroes and powers, as well as create associations between them through the HeroPower mode

├── app.py                  # Main Flask application with routes
├── models.py               # SQLAlchemy models for Hero, Power, and HeroPower
├── seeds.py                # Script to seed the database with initial data
└── migrations/             # Database migration files

Endpoint	   Method	       Description
/heroes	      GET	         List all heroes
/heroes/<id>	GET	         Get hero details with powers
/powers	      GET	         List all powers
/powers/<id>	GET	         Get power details
/powers/<id>	PATCH	       Update power description
/hero_powers	POST	       Create new hero-power relationship

Initialize the database and run migrations:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
models.py
Hero Model:
   Defines a hero table (heroes) with columns: id, name, super_name. 
   Establishes relationships with HeroPower.

Power Model:
   Defines a power table (powers) with columns: id, name, description.
   Validates that description is present and has at least 20 characters.

HeroPower Model:
   Defines an association table (hero_powers) with columns: id, hero_id, power_id, strength.
   Validates strength to be one of: 'Strong', 'Weak', 'Average'
   
Seed database: python seed.py
   Clears existing data before inserting new records.
   Seeds predefined superheroes and powers.
   Randomly assigns powers to heroes with strength levels.
   
Start server:  python app.py

Validations:
Power Descriptions
   Must be present
   Minimum 20 characters
   
HeroPower Strengths:
   Only allows: 'Strong', 'Weak', 'Average'

SerializerMixin: Alows you to easily convert SQLAlchemy model instances into dictionaries
                 Without SerializerMixin, you'd need to manually write a to_dict() method for every model, specifying which fields to include or exclude.
                 This can become tedious and repetitive. The mixin provides a reusable implementation that works across all models
                 
serialize_rules: Prevents infinite recursion in model relationships 

Use tools like Postman or curl to test each endpoint 

 HTTP Status Codes in the API
 
  200 OK: Request was successful (e.g., retrieving heroes, updating power descriptions, assigning powers).

 400 Bad Request: Invalid or missing data in the request (e.g., missing description in a power update, invalid strength value).

 404 Not Found: Requested resource does not exist (e.g., hero or power not found)


