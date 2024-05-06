#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

state_objects = list(storage.all(State).values())

if state_objects:
    first_state_id = state_objects[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No State objects found")
