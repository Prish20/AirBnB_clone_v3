#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            self.password = kwargs['password']
            del kwargs['password']
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Getter for password"""
        return self._password

    @password.setter
    def password(self, value):
        """Setter for password"""
        self._password = self.hash_password(value)

    @staticmethod
    def hash_password(password):
        """Hashes a password using MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    def to_dict(self, include_password=False):
        """Returns a dictionary representation of a User instance"""
        new_dict = super().to_dict(include_password=include_password)
        if include_password:
            new_dict["password"] = self._password
        return new_dict
