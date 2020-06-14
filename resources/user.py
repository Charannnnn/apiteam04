from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query


class User():
    def __init__(self,id,name,batch,password):
        self.id=id
        self.name=name
        self.batch=batch
        self.password=password

    @classmethod
    def getUserById(cls,id):
        result=query(f"""SELECT id,name,branch,password FROM students WHERE id='{id}'""",return_json=False)
        if len(result)>0: return User(result[0]['id'],result[0]['name'],result[0]['branch'],result[0]['password'])
        return None

class UserRegister(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id',type=str,required=True,help="ID cannot be  blank!")
        parser.add_argument('name',type=str,required=True,help="username cannot be  blank!")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="Password cannot be  blank!")
        data=parser.parse_args()
        if User.getUserById(data['id']):
            return {"message": "A user with that id already exists"}, 400
        try:
            query(f"""INSERT INTO students(id,name,branch,password)
                                  VALUES('{data['id']}','{data['name']}','{data['branch']}','{data['password']}')""")
        except:
            return {"message": "An error occurred while registering."}, 500
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('id',type=str,required=True,help="ID cannot be blank.")
    parser.add_argument('password',type=str,required=True,help="Password cannot be blank.")
    def post(self):
        data=self.parser.parse_args()
        user=User.getUserById(data['id'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.id,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

class Users(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='user_id Cannot be blank')
        data= parser.parse_args()
        try:
            return query(f"""Select * from students where id={data["id"]}""")
        except:
            return {"message": "There was an error connecting to user table"}, 500

