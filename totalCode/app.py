from flask import Flask
from flask_jwt import *
from flask_jwt_extended import *
from wsgiref.simple_server import make_server
from FullCourceProject.blueprint import api_blueprint

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

with make_server('', 5000, app) as server:
    app.register_blueprint(api_blueprint, url_prefix="")
    server.serve_forever()

# app = Flask(__name__)
# app.config["JWT_SECRET_KEY"] = "super-secret"
# jwt = JWTManager(app)
# app.register_blueprint(api_blueprint, url_prefix="")
#
# if __name__ == "__main__":
#     app.run(debug=True)
