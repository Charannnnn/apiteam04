from flask import Flask,jsonify
import pymysql
from flask_restful import Api
import logging
from flask_jwt_extended import JWTManager
from resources.user import Users,UserLogin,User,UserRegister
from resources.user_cancel import cancelBooking

from resources.admin import *

from resources.user_booking import User_Bookings_log
from resources.resource import resourceDetails

app= Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['PREFERRED_URL_SCHEME']='https'
app.config['JWT_SECRET_KEY']='sportsresourceapikey'
api= Api(app)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed.'
    }), 401


api.add_resource(Users,'/users')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(AdminLogin, '/AdminLogin')
api.add_resource(Resourcespresent, '/ResourcesPresent')
api.add_resource(AddExtraResource, '/AddExtraResource')
api.add_resource(DecrementIssuedResource, '/DecrementIssuedResource')
api.add_resource(AddReturnedResource, '/AddReturnedResource')
api.add_resource(DeleteResource, '/DeleteResource')
api.add_resource(User_Bookings_log,'/Bookings_log')
api.add_resource(cancelBooking,'/cancelBooking')
api.add_resource(resourceDetails,'/resourceDetails')

@app.route('/')
def home():
    return('Hello')
if __name__=='__main__':
    app.run(port="5000",debug=True)
