from flask import jsonify
from .model import Data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash
import os

dbPath = os.path.abspath('trojan.db')

print(f"dbPath: {dbPath}")

#initialize database session
engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)
session = Session()

class DataController:
    def readDataController(file):
        """
        Purpose: Controller that call the read_data_from_file method of the Data class
        """
        
        
        