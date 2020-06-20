from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class bookingHistory(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory1 where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d");""")
        except:
            return {"message": "There was an error connecting to the booking table"}, 500


class issuedBookings(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory1 where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status = 1 """)
        except:
            return {"message": "There was an error connecting to the booking table"}, 500


class blockedUsers(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""select
                            s.name,b.user_id,b.r_id,date_format(b.day,"%Y-%m-%d") as day,time_format(b.reservation_time,"%T") as reservation_time,
                            time_format(b.booking_time,"%T") as booking_time,
                            time_format(b.return_time,"%T") as return_time,
                            date_format(b.return_day,"%Y-%m-%d") as return_day,
                            r.resource_name as resource_name,
                            b.status,s.fine
                            from students s,booking b,resources r
                            where s.fine>0 and b.r_id=r.resource_id and b.user_id=s.id and b.day =(select max(day) from booking b1 where b1.user_id=b.user_id)
                            order by b.day;""")
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

class blockUser(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        try:
            res=query(f"""select * from students where id={data["id"]};""",return_json=False)
            if(len(res)!=0):
                query(f""" UPDATE students SET fine=50 where id= {data["id"]} """)
                return {"message":"Fine amount is now updated"},200
            return {"message": "User doen't Exist"}, 500
        except:
            return {"message": "There was an error connecting to the student table"}, 500

class bookingRequests(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory2 where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status =0;""")
        except:
            return {"message": "There was an error connecting to the booking table"}, 500

class returnedHistory(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory2 where date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and return_day is not Null ;""")
        except:
            return {"message": "There was an error connecting to the booking table"}, 500

class notreturnedHistory(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from bookingHistory2 where return_day is Null ;""")
        except:
            return {"message": "There was an error connecting to the booking table"}, 500
