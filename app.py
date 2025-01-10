from flask import Flask, redirect, request, render_template, url_for, jsonify
from .userController import HackerController
from .malwareController import MalwareController
import sys
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .model import Hacker, Data

import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))


# Create Flask application instance
app = Flask('__name__', static_folder='static')

dbPath = os.path.abspath('trojan.db')
engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)
session = Session()

hacker_controller = HackerController()
malware_controller = MalwareController()
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        result = hacker_controller.registerController(name, email, password)
        result = jsonify(result)
        # Check registration result
        if result:
            return render_template("Frontend/login.html")  # Ensure "login" route is defined
        else:
            return render_template("Frontend/register.html", error=result)           
        
    return render_template('Frontend/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Query the database for the user
            hacker = session.query(Hacker).filter_by(email=email).first()

            if hacker:
                result = hacker_controller.loginController(email=email, password=password)

                if result:
                    return redirect(url_for('dashboard', values=email))
                else:
                    return render_template('Frontend/login.html', error="Invalid password")
            else:
                return render_template('Frontend/login.html', error="User not found")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('Frontend/login.html')
    
    return render_template('Frontend/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Frontend/Dashboard.html')

@app.route('/malware')
def display_data_details():
    data = Data.read()
    if data is None:
        data = []
    return render_template('Frontend/Malware_details.html', data=data)

@app.route('/register_malware', methods=['POST'])
def register_malware():
    result = malware_controller.create_malware_record()
    return jsonify(result)



if '__name__' == '__main__':
    app.run(debug=True)