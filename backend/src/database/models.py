"""Model objects used to model data for the db

Attributes:
    DB_DIALECT: A str representing the dialect of the db
    DB_NAME: A str representing the db in which to connect to
    DB_PATH: A str representing the location of the db
    db: A SQLAlchemy service

Classes:
    Drink()
"""

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

DB_DIALECT = 'sqlite'
DB_NAME = 'database.db'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f'sqlite:///{os.path.join(PROJECT_DIR, DB_NAME)}'

db = SQLAlchemy()


def setup_db(app, db_path=DB_PATH):
    """Binds a flask application and a SQLAlchemy service

    Args:
        app: A flask app
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """Drops the database tables and starts fresh"""
    db.drop_all()
    db.create_all()


class Drink(db.Model):
    """A model representing a drink

    Attributes:
        id: An int that serves as the unique identifier for a drink
        name: A str representing the name of the drink
    """

    __tablename__ = 'drinks'

    id = Column(Integer().with_variant(Integer, 'sqlite'), primary_key=True)
    name = Column(String(80), unique=True)
    recipe = relationship('Recipe', backref='drink')

    def insert(self):
        """Inserts a new drink object into the db"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an existing question object in the db"""
        db.session.commit()

    def delete(self):
        """Deletes an existing drink object from the db"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Formats the drink as a dict

        Returns:
            drink: A dict representing the drink object
        """

        drink = {
            'id': self.id,
            'name': self.name,
            'recipe': [recipe.format() for recipe in self.recipe],
        }

        return drink


class Recipe(db.Model):
    """A model representing a recipe for a drink

    Attributes:
        id: An int that serves as the unique identifier for the recipe
        ingredient_id: The id of the ingredient that goes into the recipe
        parts: An int representing the number of parts of the drink that this
            recipe represents
        drink_id: The id of the drink that this recipe belongs to
    """

    __tablename__ = 'recipes'

    id = Column(Integer().with_variant(Integer, 'sqlite'), primary_key=True)
    ingredient_id = Column(
        Integer().with_variant(Integer, 'sqlite'),
        ForeignKey('ingredients.id')
    )
    parts = Column(Integer().with_variant(Integer, 'sqlite'))
    drink_id = Column(
        Integer().with_variant(Integer, 'sqlite'),
        ForeignKey('drinks.id')
    )

    def insert(self):
        """Inserts a new recipe object into the db"""
        db.session.add(self)
        db.session.commit()

    def format(self):
        """Formats the recipe as a dict

        Returns:
            recipe: A dict representing the recipe object
        """

        recipe = {
            'id': self.id,
            'name': self.ingredient.name,
            'color': self.ingredient.color,
            'parts': self.parts,
        }

        return recipe


class Ingredient(db.Model):
    """A model representing an ingredient that goes in recipes

    Attributes:
        id: An int that serves as the unique identifier for the ingredient
        name: A str representing the name of the ingredient
        color: A str representing the color of the ingredient
    """

    __tablename__ = 'ingredients'

    id = Column(Integer().with_variant(Integer, 'sqlite'), primary_key=True)
    name = Column(String(80), unique=True)
    color = Column(String(80))
    recipe = relationship('Recipe', backref='ingredient')

    def insert(self):
        """Inserts a new ingredient object into the db"""
        db.session.add(self)
        db.session.commit()

    def format(self):
        """Formats the ingredient as a dict

        Returns:
            ingredient: A dict representing the ingredient object
        """

        ingredient = {
            'id': self.id,
            'name': self.name,
            'color': self.color,
        }

        return ingredient
