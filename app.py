from flask import Flask
from flask import render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

symptom_reader_blueprint = Blueprint('s_reader', __name__)
app.register_blueprint(symptom_reader_blueprint)


# config SQLite

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/form', methods=['GET'])
def form():
    return render_template("user_form.html")


@app.route('/form', methods=['GET'])
def general_form():
    return render_template("general_form.html")


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Extract form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    weight = request.form['weight']
    height = request.form['height']
    medical_history = request.form.getlist('medical_history')
    symptoms = request.form.getlist('symptoms')

@app.route('/sidebar')
def sidebar():
    return render_template("sidebar.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
