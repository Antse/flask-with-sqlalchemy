# wsgi.py
import os
import logging

from flask import Flask, request, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

app = Flask(__name__)
app.config.from_object(Config)



db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Back-office', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session)) # `Product` needs to be imported before

@app.route('/hello')
def hello():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

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
