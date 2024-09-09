# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)


# class Hero(db.Model, SerializerMixin):
#     __tablename__ = 'heroes'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     super_name = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     def __repr__(self):
#         return f'<Hero {self.id}>'


# class Power(db.Model, SerializerMixin):
#     __tablename__ = 'powers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     # add validation

#     def __repr__(self):
#         return f'<Power {self.id}>'


# class HeroPower(db.Model, SerializerMixin):
#     __tablename__ = 'hero_powers'

#     id = db.Column(db.Integer, primary_key=True)
#     strength = db.Column(db.String, nullable=False)

#     # add relationships

#     # add serialization rules

#     # add validation

#     def __repr__(self):
#         return f'<HeroPower {self.id}>'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # relationships
    hero_powers = relationship('HeroPower', back_populates='hero')
    powers = association_proxy('hero_powers', 'power')

    # serialization rules
    serialize_rules = ('-hero_powers.hero', '-hero_powers.power')

    def __repr__(self):
        return f'<Hero {self.id}: {self.name} aka {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # relationships
    hero_powers = relationship('HeroPower', back_populates='power')

    # serialization rules
    serialize_rules = ('-hero_powers.power', '-hero_powers.hero')

    # validation
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return description

    def __repr__(self):
        return f'<Power {self.id}: {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    
    # foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # relationships
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    # serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be either 'Strong', 'Weak', or 'Average'.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}: {self.hero.name} with {self.power.name} as {self.strength}>'
