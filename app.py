from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
from twilio.rest import Client
import os

from dotenv import load_dotenv
load_dotenv()

client = MongoClient()
db = client.items
items = db.items


twilio_account_sid = os.getenv("account_sid")
twilio_auth_token = os.getenv("auth_token")

twilioClient = Client(twilio_account_sid, twilio_auth_token)

app = Flask(__name__)

#home page that will show many items
@app.route('/')
def store_index():
    """Show all items."""
    return render_template('store_index.html', items=items.find())

@app.route('/owner')
def owner():
    """takes user to owner landing page"""
    return render_template('owner.html', items=items.find())

@app.route('/owner/<item_id>')
def owner_view_item(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('owner_view_item.html', item=item)

@app.route('/item', methods=['POST'])
def item_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'created_at': datetime.now(),
        'in_shopping_cart': False
    }
    item_id = items.insert_one(item).inserted_id
    return render_template('owner.html', items=items.find())

@app.route('/owner/add_item')
def add_item():
    """Create a new item."""
    return render_template('item_new.html', item={}, title='New item')

@app.route('/owner/<item_id>/edit', methods=['POST'])
def edit_item(item_id):
    """edit an item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('edit_item.html', item=item, title='edit item')

@app.route('/owner/<item_id>', methods=['POST'])
def item_update(item_id):
    """Submit an edited playlist."""
    updated_item = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('owner', item_id=item_id))

@app.route('/owner/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    """Delete one item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('owner'))

#specific item
@app.route('/<item_id>')
def item_show(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_show.html', item=item)

@app.route('/shopping_cart')
def shopping_cart():
    """display user's shopping cart"""
    return render_template('shopping_cart.html', items=items.find())

@app.route('/shopping_cart/<item_id>/add_to_cart', methods=['POST'])
def add_to_shopping_cart(item_id):
    """display user's shopping cart"""
    items.update_one({'_id':ObjectId(item_id)}, {"$set": {"in_shopping_cart" : True}}, upsert=False)
    return render_template('shopping_cart.html', items=items.find())

@app.route('/shopping_cart/<item_id>/delete_from_cart', methods=['POST'])
def delete_from_shopping_cart(item_id):
    """display user's shopping cart"""
    items.update_one({'_id':ObjectId(item_id)}, {"$set": {"in_shopping_cart" : False}}, upsert=False)
    return render_template('shopping_cart.html', items=items.find())

@app.route('/shopping_cart/checkout')
def checkout():
    """display user's shopping cart"""
    return render_template('checkout.html')

@app.route('/shopping_cart/checkout/thanks')
def thanks():
    """display user's shopping cart"""
    message = twilioClient.messages.create(body="Thanks for your purchase!", from_='+18044915709', to='+14028407963')
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
