from flask import jsonify
from .model import Hacker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the database session
dbPath = os.path.abspath('trojan.db')

print(f"dbPath: {dbPath}")

engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)
session = Session()

class HackerController:
    def registerController(self, name, email, password):
        """
        Registers the given hacker (user) by calling the create method of Hacker.
        """

        try:
            
            # Call the create method of the Hacker class to register the user
            hacker = Hacker.create(name=name, email=email, password=password)
        
            # Add the hacker instance to the session
            session.add(hacker)
            
            # Commit the transaction to save the hacker in the database
            session.commit()
            
            return {"status": "success", "message": f"Hacker {name} registered successfully."}
        
        except Exception as e:
            session.rollback()
            # Handle any exceptions and return an error message
            return f"Error registering hacker: {e}"
    
    def loginController(self, email, password):
        try:
            # Query the database for the user
            hacker = session.query(Hacker).filter_by(email=email).first()

            if hacker:
                # Check the provided password against the hashed password in the database
                if check_password_hash(hacker.password, password):
                    print("login successful")
                    return jsonify({'success':'login successful', 'hacker':hacker})
                else:
                    return jsonify({"error":"Invalid email or  password"})
            else:
                return jsonify({"error":"User not found"})

        
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({f"An error occurred: {e}"})

        
    