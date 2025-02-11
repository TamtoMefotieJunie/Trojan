from flask import jsonify
from model import Hacker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the database session
dbPath = os.path.abspath('trojan2.db')

print(f"dbPath: {dbPath}")

engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)
session = Session()

class HackerController:
    def registerController(self, name, email, password):
        try:
            # Hash the password before saving it
            hashed_password = generate_password_hash(password)
            
            # Create a new Hacker instance
            hacker = Hacker(name=name, email=email, password=hashed_password)
            
            # Add and commit to the database
            session.add(hacker)
            session.commit()
            
            return {"status": "success", "message": f"Hacker {name} registered successfully."}
        except Exception as e:
            session.rollback()  # Rollback on error
            return {"status": "error", "message": f"Error registering hacker: {str(e)}"}
    
    def loginController(self, email, password):
        try:
            # Query the database for the user
            hacker = session.query(Hacker).filter_by(email=email).first()

            if hacker:
                # Check the provided password against the hashed password in the database
                if check_password_hash(hacker.password, password):
                    print("Login successful")
                    return {
                        'success': 'Login successful',
                        'hacker': {
                            'id': hacker.id,
                            'name': hacker.name,
                            'email': hacker.email
                        }
                    }
                else:
                    return {"error": "Invalid email or password"}
            else:
                return {"error": "User not found"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": str(e)}