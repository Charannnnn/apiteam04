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
    
    @classmethod
    def getAdminById(cls,id):
        result=query(f"""SELECT id,name,password FROM admin WHERE admin_id={id}""",return_json=False)
        if len(result)>0: return User(result[0]['admin_id'],result[0]['name'],result[0]['password'])
        return None


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
    def __init__(self, id, name, count, resources_available):
        self.id=id
        self.name=name
        self.count=count
        self.resources_available=resources_available

    @classmethod
    def getResourceById(cls,id):
        result=query(f"""SELECT resource_id,resource_name, count WHERE resource_id='{id}'""",return_json=False)
        if len(result)>0: 
            return Resource(result[0]['resource_id'],result[0]['resource_name'],result[0]['count'])
        return None

    @classmethod
    def getCountById(cls, id):
        result=query(f"""SELECT resource_id,resource_name, count WHERE resource_id='{id}'""",return_json=False)
        if len(result)>0:
            return Resource(result[0]['count'])
        return 0


class Resourcespresent(Resource):
    @jwt_required
    def get(self):
        try:
            return query(f"""Select * from resources""")
        except:
            return {"message": "There was an error connecting to the resource table"}, 500

class AddExtraResource(Resource):
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

class AddReturnedResource(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('count',type=int,required=True,help="Count cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        c= GetCountById(data['id'])
        r=GetResourceById(data['id'])
        try:
            if r:
                query(f"""UPDATE resource SET resources_available = resources_avaliable+1 WHERE resource_id= {data["id"]} ;""")

        except:
            return {"message": "Coudnt get resource"}, 401

class DecrementIssuedResource(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=int,required=True,help="ID cannot be blank.")
    parser.add_argument('name',type=str,required=True,help="Name cannot be blank.")
    parser.add_argument('count',type=int,required=True,help="Count cannot be blank")
    parser.add_argument('resource_available',type=int,required=True,help="Resources Available cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        r=GetResourceById(data['id'])
        try:
            if r:
                query(f"""UPDATE resource SET resources_available = resources_avaliable-1 WHERE resource_id= {data["id"]} ;""")
                # query(f"""UPDATE booking SET status = 1 WHERE r_id= {data["id"]} ;""")
        except:
            return {"message": "Coudnt issue resource"}, 401

        


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




class GetResource(Resource):
    # @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='resource_id Cannot be blank')
        parser.add_argument('name', type=str)
        parser.add_argument('count', type=int)
        parser.add_argument('resources_available', type=int)
        data= parser.parse_args()
        try:
            return query(f"""Select * from resources where resource_id={data["id"]};""")
        except:
            return {"message": "There was an error connecting to user table"}, 200



    







            
            


