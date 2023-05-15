#!/usr/bin/python3

# This module defines the User class for our application

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ 
    This class defines a user with various attributes such as email, password, first name, and last name.

    Each user can have multiple places and reviews, represented by the relationships with the Place and Review classes.
    """
    __tablename__ = 'users'
    
    # Check if the storage type is a database
    if storage_type == 'db':
        # If it's a database, create columns for the table 'users'
        # 'email', 'password', 'first_name', and 'last_name' are the user attributes
        # Establish relationships with 'Place' and 'Review'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete, delete-orphan')
    else:
        # If it's not a database, initialize the attributes as empty strings
        email = ""
        password = ""
        first_name = ""
        last_name = ""
