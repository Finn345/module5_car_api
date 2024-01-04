from flask import Blueprint, request, jsonify
from app.helpers import token_required
from app.models import db,User,Vehicle,vehicle_schema,vehicles_schema

api = Blueprint('api', __name__, url_prefix= '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value' }

@api.route('/vehicles', methods=['POST'])
@token_required
def create_vehicle(current_user_token):
    name = request.json['name']
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    year = request.json['year']
    price = request.json['price']
    serial_num = request.json['serial_num']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    
    vehicle = Vehicle(
        name=name,
        make=make,
        model=model,
        color=color,
        year=year,
        price=price,
        serial_num=serial_num,
        user_token=user_token
    )

    db.session.add(vehicle)
    db.session.commit()

    response = vehicle_schema.dump(vehicle)
    return jsonify(response)


@api.route('/vehicles/', methods=['GET'])
@token_required
def get_vehicles(current_user_token):
    owner = current_user_token.token
    vehicles = Vehicle.query.filter_by(user_token = owner).all()
    response = vehicles_schema.dump(vehicles)
    return jsonify(response)

@api.route('/vehicles/<id>', methods = ['GET'])
@token_required
def get_vehicle(current_user_token, id):
    owner = current_user_token.token
    vehicle = Vehicle.query.get(id)
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)
    
    
@api.route('/vehicles/<id>', methods = ['POST', 'PUT'])
@token_required
def update_vehicle(current_user_token,id):
    vehicle = Vehicle.query.get(id)
    
    vehicle.name = request.json['name']
    vehicle.make = request.json['make']
    vehicle.model = request.json['model']
    vehicle.color = request.json['color']
    vehicle.year = request.json['year']
    vehicle.price = request.json['price']
    vehicle.serial_num = request.json['serial_num']
    vehicle.user_token = current_user_token.token
    
    db.session.commit()
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)

@api.route('/vehicles/<id>', methods = ['DELETE'])
@token_required
def delete_vehicle(current_user_token, id):
    vehicle = Vehicle.query.get(id)
    db.session.delete(vehicle)
    db.session.commit()
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)
    