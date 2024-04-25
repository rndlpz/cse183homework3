"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

# Define the database model for the shopping list
db.define_table('shopping_list',
                Field('product_name', 'string', requires=IS_NOT_EMPTY()),
                Field('checked', 'boolean', default=False),  # Indicates whether the item is checked
                Field('user_email', default=get_user_email),  # Associate the item with the user
                Field('created_on', 'datetime', default=get_time),  # Timestamp for when the item was created
                )

# Commit changes to the database
db.commit()
