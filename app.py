from flask import redirect, url_for
from flask import render_template, request
from flask_login import login_required, current_user
from flask_migrate import Migrate

from . import create_app
from .model_f import predict_disease
from .extensions import db
from .models.healthhistory import HealthHistory
from .models.feedback import Feedback
from .recommendations import recommendations
from .auth import auth as auth_blueprint

app = create_app()
# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)
# Enable db migration
migrate = Migrate(app, db)
# push our app_context and create tables
# if they are not created yet
app.app_context().push()
with app.app_context():
    db.create_all()


@app.errorhandler(404)
# costum error handling route
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/home')
# home route
def home():
    return render_template("home.html")


@app.route('/about_us')
# about us page route
def about_us():
    return render_template("about_us.html")


@app.route('/symptom_tracking')
# symptom tracking page
@login_required
# access allow to authenticated users only
def symptom_tracking():
    # load health history fron the database
    history = HealthHistory.query.filter_by(user_id=current_user.id).all()
    # render the symptom tacking page with user's health history information
    return render_template("symp_tracking.html", history=history)


@app.route('/feedback')
# feedback page route
def feedback():
    return render_template('feedback.html')


@app.route('/feedback', methods=['POST'])
# route for feedback post handling
def feedback_post():
    # retrieve feedback from the form
    comment = request.form.get('comment')
    new_feedb = Feedback(comment=comment)
    # commit and store the feedback to database
    db.session.add(new_feedb)
    db.session.commit()
    # redirect user to hone
    return redirect(url_for('home'))


@app.route('/form', methods=['GET'])
# route for symptom check form
def form():
    return render_template("user_form.html")


@app.route('/submit_form', methods=['POST'])
# route for handling symptom checker form
def submit_form():
    # Extract form data from the form
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    # weight = request.form['weight']
    # height = request.form['height']
    symptoms = ','.join(request.form.getlist('symptoms'))
    # print(symptoms)
    # predict result bases on symptoms
    result = predict_disease(symptoms)
    if current_user.is_authenticated:
        # store prediction and metrics for authenticated user
        hist = HealthHistory(diagnosis=result, symptoms=symptoms, user_id=current_user.id)
        db.session.add(hist)
        db.session.commit()
    # print(result)
    # when success redirect to results page
    recommendations_for_result = ""
    # check for medication recommandation
    value = recommendations.get(result.strip())
    # print(value)
    if value:
        recommendations_for_result = value
    # when success redirect to results page
    return render_template('results.html', first_name=first_name, results=result,
                           recommendation=recommendations_for_result)
    # return redirect(url_for('diagnosis', result=result, first_name=first_name, last_name=last_name))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
