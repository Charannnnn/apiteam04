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

class incrementResourcesByValue(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        parser.add_argument('c', type=int, required=True, help='count Cannot be blank')
        data= parser.parse_args()
        try:
            query(f"""UPDATE resources  SET count=count+{data["c"]} and resources_available=resources_available+{data["c"]} where resource_id={data["id"]}""")
            return {"message":"changes are made to resources table","count":data["c"]}, 200
        except:
            return {"message": "There was an error connecting to resources table"}, 500

class decrementResourcesByValue(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        parser.add_argument('c', type=int, required=True, help='count Cannot be blank')
        data= parser.parse_args()
        try:
            query(f"""UPDATE resources  SET count=count-{data["c"]} and resources_available=resources_available-{data["c"]} where resource_id={data["id"]} and count>={data["count"]}""")
            return {"message":"changes are made to resources table"}, 200
        except:
            return {"message": "There was an error connecting to resources table"}, 500

class incrementResourcesByone(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        data= parser.parse_args()
        try:
            query(f"""UPDATE resources  SET resources_available=resources_available+1 where resource_id={data["id"]} and resources_available<count""")
            return {"message":"changes are made to resources table"}, 200

        except:
            return {"message": "There was an error connecting to resources table"}, 500

class decrementResourcesByone(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        data= parser.parse_args()
        try:
            query(f"""UPDATE resources  SET resources_available=resources_available-1 where resource_id={data["id"]} and resources_availabe>0""")
            return {"message":"changes are made to resources table"}, 200
        except:
            return {"message": "There was an error connecting to resources table"}, 500

class issueResource(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='student_id Cannot be blank')
        data= parser.parse_args()
        try:
            result=query(f"""select * from booking where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status=0 """,return_json=False)
            query(f"""UPDATE booking  SET status=status+1 where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status=0 """)
            if(len(result)!=0):
                data["resc_id"]=result[0]['r_id']
                query(f"""UPDATE resources  SET resources_available=resources_available-1 where resource_id={data["resc_id"]} and resources_available>0 """)
                return {"message": "updated available resources"}, 200
            else:
                return {"message":"You didn't book any  resource"},404
        except:
            return {"message": "There was an error connecting to booking table"}, 500

class acceptReturnedResource(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='student_id Cannot be blank')
        parser.add_argument('return_time', type=str, required=True, help='return_time Cannot be blank')
        data= parser.parse_args()
        query(f"""UPDATE booking  SET return_time={data["return_time"]} where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and status=1 """)
        result=query(f"""select r_id from booking where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d")""",return_json=False)
        data["resc_id"]=result[0]["r_id"]
        query(f"""UPDATE resources  SET resources_available=resources_available+1 where resource_id={data["resc_id"]}""")
        res=query(f"""select r_id from booking where user_id={data["id"]} and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d") and time_to_sec(timediff(return_time,'16:20:00'))/60 >0""",return_json=False)
        if(len(res)!=0):
            query(f"""UPDATE students  SET fine=50 where id={data["id"]}""")
            return {"message":"Fine has been added"},200
        else:
            return {"message": "updated available resources"}, 200'''
        return {"m":"ok"},200
        return {"message": "There was an error connecting to resources table"}, 500

