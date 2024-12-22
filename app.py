from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from datetime import datetime

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
swagger = Swagger(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - username
            - email
          properties:
            username:
              type: string
              description: The user's username
            email:
              type: string
              description: The user's email
    responses:
      201:
        description: User created successfully
    """
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        properties:
          id:
            type: integer
          username:
            type: string
          email:
            type: string
          created_at:
            type: string
            format: date-time
    """
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    Get a user by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: A user object
        schema:
          $ref: '#/definitions/User'
    """
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Update a user by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The user ID
      - name: body
        in: body
        required: true
        schema:
          id: User
          required:
            - username
            - email
          properties:
            username:
              type: string
              description: The user's username
            email:
              type: string
              description: The user's email
    responses:
      200:
        description: User updated successfully
    """
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: User deleted successfully
    """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Product
          required:
            - name
            - price
          properties:
            name:
              type: string
              description: The product's name
            price:
              type: number
              format: float
              description: The product's price
    responses:
      201:
        description: Product created successfully
    """
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products', methods=['GET'])
def get_products():
    """
    Get all products
    ---
    responses:
      200:
        description: A list of products
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
    definitions:
      Product:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          price:
            type: number
            format: float
          created_at:
            type: string
            format: date-time
    """
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price, 'created_at': product.created_at} for product in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """
    Get a product by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The product ID
    responses:
      200:
        description: A product object
        schema:
          $ref: '#/definitions/Product'
    """
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'created_at': product.created_at})

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """
    Update a product by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The product ID
      - name: body
        in: body
        required: true
        schema:
          id: Product
          required:
            - name
            - price
          properties:
            name:
              type: string
              description: The product's name
            price:
              type: number
              format: float
              description: The product's price
    responses:
      200:
        description: Product updated successfully
    """
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """
    Delete a product by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The product ID
    responses:
      200:
        description: Product deleted successfully
    """
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
