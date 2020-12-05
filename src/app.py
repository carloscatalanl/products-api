from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/products_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    price = db.Column(db.Integer)
    description = db.Column(db.String(100))

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

db.create_all()

# Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'description')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create product
@app.route('/products', methods=['Post'])
def create_product():
  name = request.json['name']
  price = request.json['price']
  description = request.json['description']

  new_product= Product(name, price, description)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# List all products
@app.route('/products', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result)

# List single product
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Update product
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  price = request.json['price']
  description = request.json['description']

  product.name = name
  product.price = price
  product.description = description

  db.session.commit()

  return product_schema.jsonify(product)

# Delete product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()
  return product_schema.jsonify(product)

# Index
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Flask API Ready'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)