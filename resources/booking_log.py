from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class bookingHistory(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d");""")
        except:
            return {"message": "There was an error connecting to the booking table"}, 500


class issuedBookings(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status = 1 """)
        except:
            return {"message": "There was an error connecting to the booking table"}, 500


class blockedUsers(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from students where fine>0 """)
        except:
            return {"message": "There was an error connecting to the booking table"}, 500

class unblockUser(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        try:
            res=query(f"""select * from students where id={data["id"]} and fine>0 ;""",return_json=False)
            if(len(res)!=0):
                query(f""" UPDATE students SET fine=0 where fine>0 and id= {data["id"]} """)
                return {"message":"Fine amount is now updated"},200
            return {"message": "User doen't have any Fine"}, 200
        except:
            return {"message": "There was an error connecting to the student table"}, 500
