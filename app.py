from flask import Flask
from flask import render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

symptom_reader_blueprint = Blueprint('s_reader', __name__)
app.register_blueprint(symptom_reader_blueprint)


# config SQLite
# still gonna write code, we need to decide if we creating a database or using an api
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/form')
def form():
    return render_template("user_form.html")


@app.route('/general_form')
def general_form():
    return render_template("general_form.html")


@app.route('/sidebar')
def sidebar():
    return render_template("sidebar.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
