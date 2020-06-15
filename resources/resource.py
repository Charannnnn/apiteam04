from flask_restful import Resource,reqparse
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from resources.user import Users
from datetime import date

class resourceDetails(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        data= parser.parse_args()
        try:
            return query(f"""Select * from resources where resource_id={data["id"]}""")
        except:
            return {"message": "There was an error connecting to resources table"}, 500