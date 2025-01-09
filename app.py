from flask import Flask, redirect, request, render_template, url_for, jsonify
from .userController import HackerController
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))


# Create Flask application instance
app = Flask('__name__', static_folder='static')

hacker_controller = HackerController()
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
        # Validate login credentials
        return "Login successful"
    return render_template('login.html')



if '__name__' == '__main__':
    app.run(debug=True)