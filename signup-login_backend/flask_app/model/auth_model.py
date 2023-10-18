from functools import wraps
import json
import mysql.connector
from flask import make_response, request
from datetime import datetime, timedelta
import jwt
import re
from config.config import dbconfig
class auth_model():
    def __init__(self): #connection establishment code
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("connection successful auth_model")
        except:
            print("error oooooo")

    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization = request.headers.get("Authorization")
                # print (authorization)
                if re.match("Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    # print(token)
                    try:
                        jwtdecoded=(jwt.decode(token, "arn", algorithms="HS256"))
                        # print(jwtdecoded)
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"token expired"}, 401)
                        
                    role_id = jwtdecoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_view WHERE endpoint='{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        print(json.loads(result[0]['roles']))
                        allowed_roles = json.loads(result[0]['roles'])
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"ERROR":"invalid roles"}, 404)
                    else:
                        return make_response({"ERROR":"unknown endpoint"}, 404)
                    
                else:
                    return make_response({"ERROR": "invalid token"}, 401)
            return inner2
        return inner1