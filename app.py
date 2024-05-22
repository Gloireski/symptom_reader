from flask import Flask
from flask import render_template, request
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    return 'Home page' 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)
