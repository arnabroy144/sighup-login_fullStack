import json
from flask_cors import CORS
import mysql.connector
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class user_model():
    def __init__(self): #connection establishment code
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'], database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("connection successful")
        except:
            print("error oooooo")

    def user_getall_model(self): #model function
        # business logic
        self.cur.execute("SELECT * FROM users") # "users" is name of the table querry
        result = self.cur.fetchall()
        # print(result)
        if len(result)>0:
            # return json.dumps(result)
            # return result
            res = make_response(result, 200)
            res.headers['Access-Control-Allow-Origin'] = "*" #response header for not to blobk response from other 
            return res  #for jsonify data
        else:
            return make_response({"message":"no data found"}, 204)
        
    def user_addone_model(self, data): #model function
        # business logic
        print(data['name'])
        self.cur.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')") # "users" is name of the table
        return make_response({"message":"User created successfully"}, 201)  #syntax for jsonify
    
    def user_update_model(self, data): #model function(put)
        # business logic
        print(data['name'])
        self.cur.execute(f"UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id={data['id']}") # "users" is name of the table
        if self.cur.rowcount>0:
            return make_response({"message":"User updated successfully"}, 201)
        else:
            return make_response({"message":"nothing to update"}, 202)
        
    def user_delete_model(self, id): #model function
        # business logic
        self.cur.execute(f"DELETE FROM users WHERE id={id}") # "users" is name of the table
        if self.cur.rowcount>0:
            return make_response({"message":"User deleted successfully"}, 200)
        else:
            return make_response({"message":"nothing to delete"}, 202)

    def user_patch_model(self, data, id):
        qry = "UPDATE users SET"
        for key in data:
            qry= qry+ (f" {key}='{data[key]}',")
        print (qry)
        qry = qry[:-1] +f" WHERE id={id}"

        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message": "user "+ id +" is updated successfully"}, 201)
        else:
            return make_response({"message":"nothing to update"}, 202)
        
    def user_pagination_model(self, limit, page):
        limit= int(limit)
        page=int(page)
        start= (page*limit)-limit
        qry=f"SELECT * FROM users LIMIT {start},{limit}"
        self.cur.execute(qry) # "users" is name of the table querry
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
            res = make_response({"payload":result, "page_no":page, "limit":limit}, 200)
            return res  #for jsonify data
        else:
            return make_response({"message":"no data found"}, 204)
        
    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar= '{filepath}' WHERE id = {uid} ")
        if self.cur.rowcount>0:
            return make_response({"message": "FILE UPLOADED SUCCESFULLY"}, 201)
        else:
            return make_response({"message":"nothing to update"}, 202)
         
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time  = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload= {
            "payload":userdata,
            "exp":exp_epoch_time
        }
        jwtoken= jwt.encode(payload, "arn", algorithm="HS256")
        return make_response({"token":jwtoken}, 200)
    
    def user_signup_model(self, data): #model function
        # business logic
        try:
            name = data['name']
            email = data['email']
            password = data['password']
            print(f"Received data: name={name}, email={email}, password={password}")
            self.cur.execute(f"INSERT INTO users(name,email,password) VALUES('{data['name']}', '{data['email']}', '{data['password']}')") # "users" is name of the table
            res = make_response({"message":"User created successfully"}, 201)
            res.headers['Access-Control-Allow-Origin'] = "*"  
        except KeyError as e:
            return make_response({"message": f"Missing '{e.args[0]}' field"}, 400)
         #for jsonify data
        # return make_response({"message":"User created successfully"}, 201)  #syntax for jsonify
