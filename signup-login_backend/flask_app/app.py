# .venv\Scripts\activate  **to active virtual envioronment
# $FLASK_APP="app"
# $env:FLASK_ENV="development"
# $env:PYTHONDONTWRITEBYTECODE=1
# flask run --debug
# flask run --help
from flask_cors import CORS
from flask import Flask

app=Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": ["http://192.168.29.72:3000"]}})


@app.route("/")
def welc():
    return "hellow"

@app.route("/home")
def home():
    return "hi"


from controller import * 
if __name__ == "__main__":
    app.run()