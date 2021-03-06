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


def get_user_full_name():
    name = auth.current_user.get('first_name') + " " + auth.current_user.get('last_name') if auth.current_user else "Unknown"
    return name


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
db.define_table(
    'posts',
    Field('post_desc', requires=IS_NOT_EMPTY()),
    Field('name', requires=IS_NOT_EMPTY()),
    Field('user', default=get_user_email),
)


db.commit()
