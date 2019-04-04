# wsgi.py
from flask import Flask, request
from config import Config
import os
import logging

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<int:product_id>')
def get_products(product_id):
    product = db.session.query(Product).get(product_id) # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify([product])

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_products(product_id):
    product = db.session.query(Product).get(product_id)
    db.session.delete(product)
    db.session.commit()
    return f"Well Deleted : {product.name}",202

@app.route('/products/<int:product_id>', methods=['PATCH'])
def update_products(product_id):
    req = request.get_json("name")
    name = req['name']
    product = db.session.query(Product).get(product_id)
    product.name = name
    db.session.add(product)
    db.session.commit()
    return products_schema.jsonify([product])

@app.route('/products', methods=['POST'])
def create_products():
    req = request.get_json("name")
    name = req['name']
    product = Product()
    product.name = name
    db.session.add(product)
    db.session.commit()
    return products_schema.jsonify([product])
