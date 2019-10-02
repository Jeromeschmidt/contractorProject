from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

@app.route('/')
def store_index():
    """Show all playlists."""
    return render_template('store_index.html')#, playlists=playlists.find())


if __name__ == '__main__':
    app.run(debug=True)
