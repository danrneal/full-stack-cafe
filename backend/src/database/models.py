"""Model objects used to model data for the db.

Attributes:
    DB_NAME: A str representing the db in which to connect to
    DB_PATH: A str representing the location of the db
    db: A SQLAlchemy service

Classes:
    Drink()
    Ingredient()
"""

import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

DB_NAME = "database.db"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f"sqlite:///{os.path.join(PROJECT_DIR, DB_NAME)}"

db = SQLAlchemy()


def setup_db(app, db_path=DB_PATH):
    """Binds a flask application and a SQLAlchemy service.

    Args:
        app: A flask app
        db_path: A str representing the location of the db (default: global
            DB_PATH)
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Drink(db.Model):
    """A model representing a drink.

    Attributes:
        id: An int that serves as the unique identifier for a drink
        title: A str representing the name of the drink
    """

    __tablename__ = "drinks"

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80))
    recipe = relationship("Ingredient", backref="drink")

    def insert(self):
        """Inserts a new drink object into the db."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates an existing question object in the db."""
        db.session.commit()

    def delete(self):
        """Deletes an existing drink object from the db."""
        db.session.delete(self)
        db.session.commit()

    def short_format(self):
        """Formats the drink as a dict with the recipe in short format.

        Returns:
            drink: A dict representing the drink object
        """
        drink = {
            "id": self.id,
            "title": self.title,
            "recipe": [
                ingredient.short_format() for ingredient in self.recipe
            ],
        }

        return drink

    def long_format(self):
        """Formats the drink as a dict with the recipe in long format.

        Returns:
            drink: A dict representing the drink object
        """
        drink = {
            "id": self.id,
            "title": self.title,
            "recipe": [ingredient.long_format() for ingredient in self.recipe],
        }

        return drink


class Ingredient(db.Model):
    """A model representing an ingredient for a drink.

    Attributes:
        id: An int that serves as the unique identifier for the ingredient
        name: A str representing the name of the ingredient
        parts: An int representing the number of parts of the drink that this
            ingredient represents
        color: A str representing the color of the ingredient
        drink_id: The id of the drink that this ingredient belongs to
    """

    __tablename__ = "ingredients"

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80))
    parts = Column(Integer().with_variant(Integer, "sqlite"))
    color = Column(String(80))
    drink_id = Column(
        Integer().with_variant(Integer, "sqlite"), ForeignKey("drinks.id")
    )

    def insert(self):
        """Inserts a new ingredient object into the db."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes an existing ingredient object from the db."""
        db.session.delete(self)
        db.session.commit()

    def short_format(self):
        """Formats the ingredient as a dict in a short format.

        Returns:
            ingredient: A dict representing the ingredient object
        """
        ingredient = {
            "parts": self.parts,
            "color": self.color,
        }

        return ingredient

    def long_format(self):
        """Formats the ingredient as a dict in a format that shows all details.

        Returns:
            ingredient: A dict representing the ingredient object
        """
        ingredient = {
            "name": self.name,
            "parts": self.parts,
            "color": self.color,
        }

        return ingredient
