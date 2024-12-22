from app import app, db
from flask import request, jsonify
from models import User, Product
from flasgger import swag_from

@app.route('/users', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'User',
                'required': ['username', 'email'],
                'properties': {
                    'username': {'type': 'string', 'description': "The user's username"},
                    'email': {'type': 'string', 'description': "The user's email"}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'User created successfully'}
    }
})
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of users',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/User'}
            }
        }
    },
    'definitions': {
        'User': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'username': {'type': 'string'},
                'email': {'type': 'string'},
                'created_at': {'type': 'string', 'format': 'date-time'}
            }
        }
    }
})
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at} for user in users])

@app.route('/users/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID'
        }
    ],
    'responses': {
        200: {
            'description': 'A user object',
            'schema': {'$ref': '#/definitions/User'}
        }
    }
})
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at})

@app.route('/users/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'User',
                'required': ['username', 'email'],
                'properties': {
                    'username': {'type': 'string', 'description': "The user's username"},
                    'email': {'type': 'string', 'description': "The user's email"}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'User updated successfully'}
    }
})
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The user ID'
        }
    ],
    'responses': {
        200: {'description': 'User deleted successfully'}
    }
})
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/products', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Product',
                'required': ['name', 'price'],
                'properties': {
                    'name': {'type': 'string', 'description': "The product's name"},
                    'price': {'type': 'number', 'format': 'float', 'description': "The product's price"}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Product created successfully'}
    }
})
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of products',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/Product'}
            }
        }
    },
    'definitions': {
        'Product': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'price': {'type': 'number', 'format': 'float'},
                'created_at': {'type': 'string', 'format': 'date-time'}
            }
        }
    }
})
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price, 'created_at': product.created_at} for product in products])

@app.route('/products/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The product ID'
        }
    ],
    'responses': {
        200: {
            'description': 'A product object',
            'schema': {'$ref': '#/definitions/Product'}
        }
    }
})
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'created_at': product.created_at})

@app.route('/products/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The product ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Product',
                'required': ['name', 'price'],
                'properties': {
                    'name': {'type': 'string', 'description': "The product's name"},
                    'price': {'type': 'number', 'format': 'float', 'description': "The product's price"}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Product updated successfully'}
    }
})
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The product ID'
        }
    ],
    'responses': {
        200: {'description': 'Product deleted successfully'}
    }
})
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
