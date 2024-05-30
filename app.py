import os

from flask import Flask, flash, redirect, url_for
from flask import render_template, request, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt, check_password_hash

from .extensions import db
from .models.user import User

# from config import Config
bcrypt = Bcrypt()


def create_app():
    app_ = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app_.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app_.config["SECRET_KEY"] = 'cc0f7589be8f11e1082328d160892d8a'
    # app_.config.from_object(Config)
    db.init_app(app_)
    bcrypt.init_app(app_)
    return app_


app = create_app()
# db = SQLAlchemy(app)
migrate = Migrate(app, db)
# manager = Manager(app)
# db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()

symptom_reader_blueprint = Blueprint('s_reader', __name__)
app.register_blueprint(symptom_reader_blueprint)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username required!'),
                                                   Length(min=5, max=25,
                                                          message='Username must be in 5 to 25 characters')])
    password = PasswordField('Password', validators=[InputRequired('Password required')])

    # submit = SubmitField('Submit')

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(
            username=self.username.data
        ).first()
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        # Do the passwords match
        if not self.user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        return True


# config SQLite


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_post():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash("You have been logged in.", category="success")
    #
    #     username = form.name.data
    #     password = form.password.data
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    print(user)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/landing')
def landing_page():
    return render_template("landng_page.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists')
        return redirect(url_for('register'))
    new_user = User(username=username, firstName=firstname, lastName=lastname)
    print(new_user)
    new_user.set_password(password)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


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
    medical_history = ','.join(request.form.getlist('medical_history'))
    symptoms = ','.join(request.form.getlist('symptoms'))

#when success redirect to results page
    return redirect(url_for('diagnosis', results='#'))


@app.route('/diagnosis/<int:#>')
def results(user_id):
    user_name, results = get_user_data(user_id)
    return render_template('sidebar.html', user_name=user_name, results=results)


@app.route('/sidebar')
def sidebar():
    return render_template("sidebar.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
