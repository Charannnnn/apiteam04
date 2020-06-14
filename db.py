from decimal import Decimal
import pymysql
from flask import jsonify
def query(querystr, return_json=True):
    connection= pymysql.connect(
                                host='skillup-team-04.cxgok3weok8n.ap-south-1.rds.amazonaws.com',
                                user='admin',
                                password='coscskillup',
                                db='sports_utilities',
        cursorclass=pymysql.cursors.DictCursor

    )
    connection.begin()
    cursor=connection.cursor()
    cursor.execute(querystr)
    result= encode(cursor.fetchall())
    connection.commit()
    cursor.close()
    connection.close()
    if return_json:
        return jsonify(result)
    else:
        return result

def encode(data):
    for row in data:
        for key,value in row.items():
            if isinstance(value, Decimal):
                row[key]=str(value)
    return data