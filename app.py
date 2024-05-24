from flask import Flask
from flask import render_template, request, Blueprint

app = Flask(__name__)

symptom_reader_blueprint = Blueprint('s_reader', __name__)
app.register_blueprint(symptom_reader_blueprint)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
