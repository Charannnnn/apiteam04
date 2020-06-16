from flask_restful import Resource,reqparse
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from resources.user import Users
from datetime import date
class User_Bookings_log(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        result=[]
        try:
            log1= query(f"""Select * from bookingHistory where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d")""",return_json=False)
            log2= query(f"""Select * from bookingHistory where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(DATE_SUB(date_format(curdate(),"%Y-%m-%d"),INTERVAL 1 day),"%Y/%m/%d")""",return_json=False)
            if(len(log1)!=0):
                result.append(log1)
            if(len(log2)!=0):
                result.append(log2)
            return jsonify(result)

        except:
            return {"message": "There was an error connecting to bookings table"}, 500



