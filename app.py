from flask import Flask
import pymysql
from flask_restful import Api
from resources.user import User

app= Flask(__name__)
api= Api(app)

api.add_resource(User,'/user')

@app.route('/')
def home():
    return('Hello')


if __name__=='__main__':
    app.run()