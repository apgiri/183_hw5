"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email

url_signer = URLSigner(session)


@action('index')
@action.uses(db, auth, url_signer, 'index.html')
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        # test pycharm connection
        load_posts_url=URL('load_posts', signer=url_signer),
        add_post_url=URL('add_post', signer=url_signer),
        delete_post_url=URL('delete_post', signer=url_signer),
    )


# first API function: used to answer requests from JS in browser
@action('load_posts')
@action.uses(db, auth, url_signer.verify())
def load_posts():
    rows = db(db.posts).select().as_list()
    return dict(rows=rows)


# second API function: used to answer add_post requests from JS in browser
@action('add_post', method="POST")
@action.uses(db, url_signer.verify())
def add_post():

    row = db(db.auth_user.email == get_user_email()).select().first()
    name = row.first_name + " " + row.last_name if row is not None else "Unknown"

    id = db.posts.insert(
        post_desc=request.json.get('post_desc'),
        name=name,
    )
    return dict(id=id, name=name)


