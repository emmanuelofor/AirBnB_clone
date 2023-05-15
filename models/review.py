#!/usr/bin/python3

# This is the Review module for our application

from sqlalchemy.sql.schema import ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from models import storage_type

class Review(BaseModel, Base):
    """ 
    This is the Review class, it stores review information.

    Each review is associated with a place and a user.
    """
    __tablename__ = 'reviews'

    # Check if the storage type is a database
    if storage_type == 'db':
        # If it's a database, create columns for the table 'reviews'
        # 'text' is the review content, 'place_id' is the id of the associated place,
        # and 'user_id' is the id of the user who made the review.
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        # If it's not a database, initialize the attributes as empty strings
        place_id = ""
        user_id = ""
        text = ""
