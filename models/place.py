#!/usr/bin/python3

# This is the module for managing "Place" in our application

from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship

# Check if the storage type is database
if storage_type == 'db':
    # If yes, create a place_amenity table to establish many-to-many relationship between place and amenity
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )


class Place(BaseModel, Base):
    """ This class represents a place where guests can stay """
    __tablename__ = 'places'
    if storage_type == 'db':
        # If the storage type is database, these are the columns for the place table
        # Each column represents a different attribute of the place
        # Relationships are established with cities, users, reviews, and amenities
    else:
        # If the storage type is not database, set default values for attributes
        # Define relationships with reviews and amenities as property methods

        @property
        def reviews(self):
            ''' This method returns a list of review instances that have the same place_id as the current Place.id
                It represents a relationship between Place and Review in a file storage system.
            '''
            from models import storage
            all_revs = storage.all(Review)
            lst = []
            for rev in all_revs.values():
                if rev.place_id == self.id:
                    lst.append(rev)
            return lst

        @property
        def amenities(self):
            ''' This method returns a list of Amenity instances linked to the current Place.
                It uses the attribute amenity_ids that contains all Amenity.id linked to the Place.
            '''
            from models import storage
            all_amens = storage.all(Amenity)
            lst = []
            for amen in all_amens.values():
                if amen.id in self.amenity_ids:
                    lst.append(amen)
            return lst

        @amenities.setter
        def amenities(self, obj):
            ''' This method allows adding an Amenity.id to the attribute amenity_ids.
                It accepts only Amenity objects.
            '''
            if obj is not None:
                if isinstance(obj, Amenity):
                    if obj.id not in self.amenity_ids:
                        self.amenity_ids.append(obj.id)

