#!/usr/bin/env python3
"""function that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new _id"""
    new_doc = kwargs
    result = mongo_collection.insert_one(new_doc)
    return result.inserted_id
