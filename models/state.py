#!/usr/bin/python3

# This module manages "State" in our application

from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ This class represents a state in our application """
    __tablename__ = 'states'
    
    # Check if the storage type is a database
    if storage_type == 'db':
        # If it's a database, create a 'name' column for the 'states' table
        # Also, establish a relationship with 'City'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        # If it's not a database, initialize the 'name' attribute as an empty string
        # And define a method to get all cities related to this state
        name = ''

        @property
        def cities(self):
            ''' This method returns a list of City instances that are related to the current State.
                It represents a relationship between State and City in a file storage system.
            '''
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities
