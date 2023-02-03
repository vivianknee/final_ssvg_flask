""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


class Car(db.Model):
    __tablename__ = 'cars'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, unique=True, primary_key=True)
    _type = db.Column(db.String(255), unique=False, nullable=False)
    _engine = db.Column(db.String(255), unique=False, nullable=False)
    _price = db.Column(db.Integer, unique=False, nullable=False)
   

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, type, engine, price):
        self._type = type    # variables with self prefix become part of the object, 
        self._engine = engine
        self._price = price
        #self.determine_value()

    # gets the type of the manufacturer or the car
    @property
    def type(self):
        return self._type
    
    # a setter function, allows type to be updated after initial object creation
    @type.setter
    def type(self, type):
        self._type = type
    
    # a engine getter
    @property
    def engine(self):
        return self._engine

    # a setter function to set the car's engine
    @engine.setter
    def engine(self, engine):
        self._engine = engine
    
     # a price getter
    @property
    def price(self):
        return self._price

    # a setter function to set the car's price 
    @price.setter
    def price(self, price):
        self._price = price
        #self.determine_value() #calls function whenever price of car changes 
         
    # @property
    # def value(self):
    #     return self._value
    
    #determines car value based on price and stores it by assigning it to object
    def determine_value(self):
        if self._price > 60000:
            self._value = "Luxury Car"
        elif self._price in range(30000, 60000):
            self._value ="Middle-end Car"
        else:
            self._value ="Low-end/Second-hand Car"
            
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "type" : self.type,
            "engine" : self.engine,
            "price" : self.price
           # "value" : self.value
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, engine="", type="", price=""):
        """only updates values with length"""
        if len(type) > 0:
            self.type = type
        if len(engine) > 0:
            self.engine = engine
        self.price = price
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initCars():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    c1 = Car(engine='ice', type='truck', price=10000)
    c2 = Car(engine='electric', type='suv', price=50000) 


    cars = [c1, c2]

    """Builds sample car/note(s) data"""
    for car in cars:
        try:
            car.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {car.model}")

