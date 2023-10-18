from flask_cors import cross_origin
from app import app
from flask import request
from flask import send_file
from model.user_model import user_model
from model.auth_model import auth_model
from datetime import datetime

obj =user_model()
auth = auth_model()

@app.route("/user/getall")  # (read operation)
# @auth.token_auth()
def user_getall_controller():  # Request handler function 
    return obj.user_getall_model()

@app.route("/user/addone", methods=["post"]) #(creat operation)
def user_addone_controller():  # Request handler function
    #print(request.form)
    return obj.user_addone_model(request.form)

@app.route("/user/update", methods=["put"]) #(updatr operation)
@auth.token_auth()
def user_update_controller():  # Request handler function
    #print(request.form)
    return obj.user_update_model(request.form)

@app.route("/user/delete/<id>", methods=["delete"]) #(delete operation)
def user_delete_controller(id):  # Request handler function
    #print(request.form)
    return obj.user_delete_model(id)

@app.route("/user/patch/<id>", methods=["patch"]) #(update operation only required row)
def user_patch_controller(id):  # Request handler function
    #print(request.form)
    return obj.user_patch_model(request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods=["get"])  # (pagination operation)
def user_pagination_controller(limit, page):  # Request handler function 
    return obj.user_pagination_model(limit, page)

@app.route("/user/<uid>/upload/avatar", methods=["put"])  # ( operation)
def user_upload_avatar_controller(uid):  # Request handler function 
    file= (request.files['avatar'])
    unicfilename= str(datetime.now().timestamp()).replace(".", "")
    splitfilename= file.filename.split(".")
    ext= splitfilename[len(splitfilename)-1]
    finalfilepath= (f"uploads/{unicfilename}.{ext}")
    file.save(finalfilepath)
    return obj.user_upload_avatar_model(uid, finalfilepath)

@app.route("/uploads/<filename>")
def user_getavatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login", methods=["post"])
def user_login_conttroller():
    # request.form
    return obj.user_login_model(request.form)

@app.route("/user/signup", methods=["post"])
# @cross_origin()
def user_signup_conttroller():
    # request.form
    return obj.user_signup_model(request.form)