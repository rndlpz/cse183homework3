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
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        load_data_url = URL('load_data'),
        add_item_url = URL('add_item'),
        mark_purchased_url = URL('mark_purchased'),
        delete_item_url = URL('delete_item')
    )

@action('load_data')
@action.uses(db, auth.user)
def load_data():
    user_email = get_user_email()
    if user_email:
        user_id = auth.current_user.get('id')
        query = (db.shopping_list.user_email == user_email) & (db.shopping_list.user_id == user_id)
        items = db(query).select(orderby=~db.shopping_list.purchased)
        return dict(items=items)
    else:
        return dict(items=[])

@action('add_item', method='POST')
@action.uses(db, auth.user, url_signer.verify())
def add_item():
    user_email = get_user_email()
    user_id = auth.current_user.get('id')
    if user_email:
        name = request.json.get('name')
        if name:
            item_id = db.shopping_list.insert(name=name, purchased=False, user_email=user_email, user_id=user_id)
            item = db.shopping_list(item_id)
            return dict(id=item.id, name=item.name, purchased=item.purchased)
        else:
            abort(400, 'Name is required')
    else:
        abort(403)

@action('mark_purchased/<item_id>', method='PUT')
@action.uses(db, auth.user, url_signer.verify())
def mark_purchased(item_id):
    user_email = get_user_email()
    user_id = auth.current_user.get('id')
    if user_email:
        item = db.shopping_list(item_id)
        if item and item.user_email == user_email and item.user_id == user_id:
            item.update_record(purchased=not item.purchased)
            return dict(success=True)
        else:
            abort(404, 'Item not found')
    else:
        abort(403)

@action('delete_item/<item_id>', method='DELETE')
@action.uses(db, auth.user, url_signer.verify())
def delete_item(item_id):
    user_email = get_user_email()
    user_id = auth.current_user.get('id')
    if user_email:
        item = db.shopping_list(item_id)
        if item and item.user_email == user_email and item.user_id == user_id:
            item.delete_record()
            return dict(success=True)
        else:
            abort(404, 'Item not found')
    else:
        abort(403)
