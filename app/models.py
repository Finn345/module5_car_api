from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 


login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable = False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, unique=True, default='')
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    vehicle = db.relationship('Vehicle', backref='owner', lazy=True)
    
    def __init__(self, email, first_name='', last_name='', id = '',  password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.token = self.set_token(10)
        self.g_auth_verify = g_auth_verify
        
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'The user {self.email} has been added!'
    
class Vehicle(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150), nullable=False, default='')
    make = db.Column(db.String(150), nullable=False, default='')
    model = db.Column(db.String(150), nullable=False, default='')
    color = db.Column(db.String(150), nullable=False, default='')
    year = db.Column(db.Numeric(precision=4))
    price = db.Column(db.Numeric(precision=10,scale=2))
    serial_num = db.Column(db.Numeric(precision=17))
    user_token = db.Column(db.String, db.ForeignKey(User.token), nullable=False)
    
    def __init__(self, make, model, color, year, price, serial_num, user_token, name, id=''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.price = price
        self.serial_num = serial_num
        self.user_token = user_token
        self.name = name
        
    def __repr__(self):
        return f'The following vehicle has been added: {self.name}.'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
class VehicleSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model','color','year','price', 'serial_num', 'name']
        
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)