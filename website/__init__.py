#Import các thư viện vào
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app=app)
# Thiết lập SECRET_KEY cho app
app.config["SECRET_KEY"] = "@#@$@%#^#&*%^(#*&%^*&@*%@(%@"
# Đổi lại root:password theo MYSQL trên máy từng người để có thể tạo database
app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123qwe@localhost/phongmachtu?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
