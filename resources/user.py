from flask_restful import Resource, reqparse
from db import query

class User(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='Cannot be blank')
        data= parser.parse_args()
        try:
            return query(f"""Select * from sports_utilities.user where user_id={data["user_id"]}""")
        except:
            return {"message": "There was an error connecting to user table"}, 500

