from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from app import db

class Hero(db.Model, SerializerMixin):
    __tablename__ = "heroes"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='hero', cascade="all, delete-orphan")

class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='power', cascade="all, delete-orphan")
    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description must be present")
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class HeroPower(db.Model,  SerializerMixin):
     __tablename__ = 'hero_powers'

     id = db.Column(db.Integer, primary_key=True)
     strength = db.Column(db.String, nullable=False)
     hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
     power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
     
     serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
     @validates('strength')
     def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength

     def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "power": self.power.to_dict(),
        }
