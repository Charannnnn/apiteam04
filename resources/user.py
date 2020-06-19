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
            return {"message": "There was an error connecting to user table"}, 200

class bookResource(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id',type=str,required=True,help="ID cannot be  blank!")
        parser.add_argument('name',type=str,required=True,help="resource_name cannot be  blank!")
        parser.add_argument('day',type=str,required=True,help="date cannot be left blank!")
        parser.add_argument('reservation_time',type=str,required=True,help="reservation_time  cannot be  blank!")
        #parser.add_argument('booking_time',type=str,required=True,help="booking_time  cannot be  blank!")
        #parser.add_argument('return_time',type=str)
        data=parser.parse_args()
        res=query(f"""select fine from students where id='{data["id"]}';""",return_json=False)
        if(res[0]['fine']>0):
            return {"message":"You can't book the resource until your due is cleared"},400
        log=query(f"""select resource_id,resources_available from resources where resource_name='{data["name"]}';""",return_json=False)
        log1=query(f"""select * from bookingHistory1 where user_id='{data["id"]}' and date_format(day,"%Y-%m-%d")=date_format(curdate(),"%Y-%m-%d")""",return_json=False)
        log2=query(f""" select date_format('{data['day']}',"%Y-%m-%d")=curdate() as dif; """,return_json=False)
        #a=len(log)
        #b=len(log1)
        c=log2[0]['dif']
        if(len(log)!=0 and len(log1)==0 and c==1 and log[0]['resources_available']>0):
            try:
                query(f"""INSERT INTO booking(user_id,r_id,day,reservation_time,status)
                                    VALUES('{data['id']}',CAST({log[0]['resource_id']} as UNSIGNED),date_format('{data['day']}',"%Y-%m-%d"),
                                        time_format('{data['reservation_time']}',"%T"),0);""")

                return {"message": "Booking is successful."}, 201
            except:
                return {"message": "An error occurred while booking."}, 400
        else:
            return {"message": "Resource is not available for you now,try to book after some time."}, 400


'''class bookResource(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('id',type=str,required=True,help="ID cannot be  blank!")
        parser.add_argument('name',type=str,required=True,help="resource_name cannot be  blank!")
        parser.add_argument('day',type=str,required=True,help="date cannot be left blank!")
        parser.add_argument('reservation_time',type=str,required=True,help="reservation_time  cannot be  blank!")
        parser.add_argument('booking_time',type=str,required=True,help="booking_time  cannot be  blank!")
        parser.add_argument('return_time',type=str)
        data=parser.parse_args()
        res=query(f"""select fine from students where id='{data["id"]}';""",return_json=False)
        if(len(res)==0):
            return {"message":"You can't book the resource until your due is cleared"},400
        log=query(f"""select resource_id,resources_available from resources where resource_name='{data["name"]}';""",return_json=False)
        if(len(log)!=0 and log[0]['resources_available']>0):
            if(data['return_time']!=None):
                #try:
                query(f"""INSERT INTO booking
                                    VALUES('{data['id']}',CAST({log[0]['resource_id']} as UNSIGNED),date_format('{data['day']}',"%Y-%m-%d"),
                                        time_format('{data['reservation_time']}',"%T"),time_format('{data['booking_time']}',"%T"),
                                        time_format('{data['return_time']}',"%T"),CAST(0 as UNSIGNED))""")
                return {"message": "User created successfully."}, 201

                #except:
                    #return {"message": "An error occurred while registering."}, 500
            else:
                #try:
                query(f"""INSERT INTO booking(user_id,r_id,day,reservation_time,booking_time,status)
                                    VALUES('{data['id']}',CAST({log[0]['resource_id']} as UNSIGNED),date_format('{data['day']}',"%Y-%m-%d"),
                                        time_format('{data['reservation_time']}',"%T"),time_format('{data['booking_time']}',"%T"),CAST(0 as UNSIGNED))""")

                return {"message": "User created successfully."}, 201
                #except:
                    #return {"message": "An error occurred while registering."}, 500
        else:
            return {"message": "Resource is not available now,try to book after some time."}, 400'''








    
    
    


