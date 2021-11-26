import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask import render_template
from website import app


@app.route('/')
def home():
    return render_template('home.html')


# Xử lí các trang
#--------------------NGƯỜI DÙNG---------------------


#--------------------Y TÁ---------------------
@app.route('/yta/home')
def yta_home():
    return render_template('yta.html')


#--------------------BÁC SĨ--------------------

#--------------------ADMIN---------------------


def create_app():
    return app