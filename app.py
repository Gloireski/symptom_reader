import os
from datetime import timedelta

from flask import Flask, flash, redirect, url_for
from flask import render_template, request, Blueprint
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt, check_password_hash

from .model_f import predict_disease
from .extensions import db
from .models.user import User
from .models.healthhistory import HealthHistory
from .recommendations import recommendations

# from config import Config
bcrypt = Bcrypt()


def create_app():
    app_ = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # sqlite db path, point to current project folder path
    app_.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app_.config["SECRET_KEY"] = 'cc0f7589be8f11e1082328d160892d8a'
    # help logout user after 15 minutes
    app_.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app_)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

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

        # Does our user exist
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
# @login_required
def home():
    return render_template("Home_page.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    # print(user)
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    login_user(user, remember=remember)
    return redirect(url_for('home'))


@app.route('/landing')
def landing_page():
    return render_template("landng_page.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/symptom_tracking')
@login_required
def symptom_tracking():
    history = HealthHistory.query.filter_by(user_id=current_user.id).all()
    print(history)
    return render_template("symp_tracking.html", history=history)


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
    # print(new_user)
    new_user.set_password(password)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/diagnosis/<result>/<first_name>', methods=['GET', 'POST'])
def diagnosis(result, first_name):
    # user_name, results = get_user_data(user_id)
    # print(results)
    # recommendations_for_result = {recommendations[result] for recommendation in recommendations if
    #                               recommendation == result}
    recommendations_for_result = ""
    value = recommendations.get(result)
    if value:
        recommendations_for_result = value
    return render_template('sidebar.html', first_name=first_name, results=result,
                           recommendation=recommendations_for_result)


@app.route('/form', methods=['GET'])
def form():
    return render_template("user_form.html")


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Extract form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    weight = request.form['weight']
    height = request.form['height']
    medical_history = ','.join(request.form.getlist('medical_history'))
    symptoms = ','.join(request.form.getlist('symptoms'))
    # print(symptoms)
    result = predict_disease(symptoms)
    if current_user.is_authenticated:
        hist = HealthHistory(diagnosis=result, symptoms=symptoms, user_id=current_user.id)
        db.session.add(hist)
        db.session.commit()
    # print(result)
    # when success redirect to results page
    return redirect(url_for('diagnosis', result=result, first_name=first_name))


@app.route('/results')
def sidebar():
    return render_template("sidebar.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
