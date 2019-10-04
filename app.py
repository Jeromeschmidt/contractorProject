from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

client = MongoClient()
db = client.items
items = db.items

app = Flask(__name__)

#home page that will show many items
@app.route('/')
def store_index():
    """Show all items."""
    return render_template('store_index.html', items=items.find())

@app.route('/owner')
def owner():
    """takes user to owner landing page"""
    return render_template('owner.html')

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
        'created_at': datetime.now()
    }
    print(item)
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('item_show', item_id=item_id))

@app.route('/owner/add_item')
def item():
    """Create a new item."""
    return render_template('item_new.html', item={}, title='New item')

@app.route('/owner/edit_item')
def edit_item():
    """edit an item."""
    return render_template('edit_item.html', item={}, title='edit item')

@app.route('/owner/<item_id>', methods=['POST'])
def item_delete(item_id):
    """Delete one item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('store_index'))

#specific item
@app.route('/<item_id>')
def item_show(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_show.html', item=item)

@app.route('/shopping_cart')
def shopping_cart():
    """display user's shopping cart"""
    return render_template('shopping_cart.html')

@app.route('/shopping_cart/checkout')
def checkout():
    """display user's shopping cart"""
    return render_template('checkout.html')

@app.route('/shopping_cart/checkout/thanks')
def thanks():
    """display user's shopping cart"""
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
