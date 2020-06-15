from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
from resources.user import User
class Admin(Resource):
    def __init__(self,id,name,password):
        self.id=id
        self.name=name
        self.password=password


class AdminLogin(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('password',type=str,required=True,help="Password cannot be blank.")
    def post(self):
        data=self.parser.parse_args()
        admin=Admin.getUserById(data['id'])
        if admin and safe_str_cmp(admin.password,data['password']) and safe_str_cmp(admin.name, data['name']):
            access_token=create_access_token(identity=admin.id,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

class Resource(Resource):
    def __init__(self, id, name, count):
        self.id=id
        self.name=name
        self.count=count

    @classmethod
    def getResourceById(cls,id):
        result=query(f"""SELECT resource_id,resource_name, count WHERE resource_id='{id}'""",return_json=False)
        if len(result)>0: 
            return Resource(result[0]['resource_id'],result[0]['resource_name'],result[0]['count'])
        return None

    @classmethod
    def getCountById(cls, id);
    result=query(f"""SELECT resource_id,resource_name, count WHERE resource_id='{id}'""",return_json=False)
    if len(result)>0: 
        return Resource(result[0]['count'])
    return 0


class Resourcespresent(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        try:
            return query(f"""Select * from resources"""), 200
        except:
            return {"message": "There was an error connecting to the resource table"}, 500

class AddResource(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('count',type=int,required=True,help="Count cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        r=Resource.getResourceById(data['id'])
        try:
            if r:
                query(f"""UPDATE resource SET count = count+1 WHERE resource_id= {data["id"]} ;""")
            else:
                query(f"""INSERT into resource values({data["id"]}, {data["name"]}, {data["count"]});""")
        except:
            return {"message": "Coudnt add resource"}, 401

class DeleteResource(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('count',type=int,required=True,help="Count cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        r=Resource.getResourceById(data['id'])
        try:
            if r:
                query(f"""UPDATE resource SET count = count-1 WHERE resource_id= {data["id"]} ;""")
            else:
                query(f"""DELETE from resource WHERE resource_id= {data["id"]};""")
        except:
            return {"message": "Coudnt delete resource"}, 500


class AddUser(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('user_id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('r_id',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('day',type=int,required=True,help="Count cannot be blank")
    parser.add_argument('reservation_time',type=int,required=True,help="Count cannot be blank")
    parser.add_argument('booking_time',type=int,required=True,help="Count cannot be blank")
    parser.add_argument('return_time',type=int,required=True,help="Count cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        user= User.getUserById(data['user_id'])
        count= Resource.getCountById(data['r_id'])
        try:
            if user!=None and count:
                query(f"""INSERT INTO booking values({data['user_id']}, {data['r_id']}, {data['day']}, 
                {data['reservation_time']}, {data['booking_time']}, {data['return_time']});""")
        except:
            return {"message": "Coudnt add user"}, 500

    







            
            


