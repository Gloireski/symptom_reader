from flask import Flask
from flask import render_template, request, Blueprint
from flask_sqlalchemy import SQLAlchemy

from Config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # db.init_app(app)
    return app


app = create_app()
db = SQLAlchemy(app)
# db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()

symptom_reader_blueprint = Blueprint('s_reader', __name__)
app.register_blueprint(symptom_reader_blueprint)


# config SQLite
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/landing')
def landing_page():
    return render_template("landng_page.html")


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
