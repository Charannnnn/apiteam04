from resources.user import *
from resources.resource import *
from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query



class BookResource:
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('count',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('resources_available',type=str,required=True,help="Name cannot be blank.")
    
    
    def post():
        data=self.parser.parse_args()
        user=User.getUserById(data['id'])
        available= resource_.check_available_resources(data['id'])
        try:
            
            

