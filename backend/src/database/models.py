"""Model objects used to model data for the db

Attributes:
    DB_DIALECT: A str representing the dialect of the db
    DB_NAME: A str representing the db in which to connect to
    DB_PATH: A str representing the location of the db
    db: A SQLAlchemy service

Classes:
    Drink()
"""

import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

DB_DIALECT = 'sqlite'
DB_NAME = 'database'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = f'sqlite:///{os.path.join(PROJECT_DIR, DB_NAME)}'

db = SQLAlchemy()


def setup_db(app):
    """Binds a flask application and a SQLAlchemy service

    Args:
        app: A flask app
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_NAME
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string,'name':string,'parts':number}]
    recipe = Column(String(180), nullable=False)

    def short(self):
        '''
        short()
            short form representation of the Drink model
        '''
        print(json.loads(self.recipe))
        short_recipe = [
            {
                'color': r['color'],
                'parts': r['parts']
            } for r in json.loads(self.recipe)
        ]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        '''
        long()
            long form representation of the Drink model
        '''
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

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

    def __repr__(self):
        return json.dumps(self.short())
