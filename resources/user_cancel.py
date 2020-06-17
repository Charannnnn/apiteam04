from flask_restful import Resource,reqparse
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from resources.user import Users
from datetime import date

class cancelBooking(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        result={}
        try:
            log1=query(f"""Select * from bookingHistory where user_id={data["id"]} and  date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status=0""",return_json=False)
            
            if(len(log1)==0):
                return {"message": "Can't Cancel your booking request"}, 500
            else:
                query(f"""DELETE from booking where user_id={data["id"]} and  date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status=0""")
                result["1"]=log1
                result["message"]="Your booking has been canceled !!"
                return jsonify(result)
        except:
            return {"message": "Cannot connect to the bookings table"}, 500