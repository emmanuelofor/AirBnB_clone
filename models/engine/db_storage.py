#!/usr/bin/python3

# This module represents the database storage engine for our application.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    # If the storage type is a database, import the 'place_amenity' table from 'place' module
    from models.place import place_amenity

# Define a dictionary that maps class names to their corresponding classes
classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    '''
    This class represents the database storage engine for MySQL storage.

    It provides methods for querying, adding, deleting, and committing changes to the database.
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
        Instantiate a new DBStorage instance.

        It creates a connection to the MySQL database based on the environment variables.
        '''
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        # Create the engine for connecting to the MySQL database
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB
            ), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            # Drop all tables if the environment is set to 'test'
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        Query the current database session for objects of a specific class or all classes.

        This method returns a dictionary:
        - Key: <class-name>.<object-id>
        - Value: object
        '''
        dct = {}

        if cls is None:
            # If cls is not specified, query all classes
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            # If cls is specified, query only that class
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj

        return dct

    def new(self, obj):
        '''
        Add the object to the current database session.
        '''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        '''
        This method commits the changes to the database.
        '''
        self.__session.commit()

    def delete(self, obj=None):
    '''
    Delete the object from the current database session.

    If obj is not None, it deletes the specific object.
    '''
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
    '''
    Reload the database.

    It creates the database tables and establishes a new database session.
    '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
    '''
    Close the working SQLAlchemy session.

    This method closes the current SQLAlchemy session.
    '''
        self.__session.close()    

