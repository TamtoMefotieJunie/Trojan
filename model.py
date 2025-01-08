from sqlalchemy import create_engine, select, MetaData, Table, Column, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

dbPath = 'trojan.db'
engine = create_engine('sqlite:///%s' % dbPath)
metadata = MetaData()

# Hacker Table Definition
HackerTable = Table(
    'Hacker', metadata,
    Column('id', String(60), primary_key=True),
    Column('name', String(60)),
    Column('email', String(60), unique=True),
    Column('password', String(255))
)

class Hacker:

    'table_name' = 'Hacker'
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    def _init_(self, id=None, name=None, email=None, password=None):
        self.id = id or str(uuid.uuid4())  # Auto-generate a UUID if not provided
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def create(name, email, password):

        """Register a new hacker."""
        
        hashed_password = generate_password_hash(password)
        hacker = {
            'id': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password': hashed_password
        }
        stmt = HackerTable.insert().values(hacker)
        with engine.connect() as conn:
            conn.execute(stmt)
        return f"Hacker {name} registered successfully."

    @staticmethod
    def login(email, password):
        """Log in a hacker by validating their email and password."""
        with engine.connect() as conn:
            stmt = HackerTable.select().where(HackerTable.c.email == email)
            result = conn.execute(stmt).fetchone()
        if result:
            stored_password = result['password']
            if check_password_hash(stored_password, password):
                return f"Welcome, {result['name']}!"
            else:
                return "Incorrect password."
        return "Hacker not found."

    @staticmethod
    def read():
        """Read all hackers."""
        with engine.connect() as conn:
            stmt = HackerTable.select()
            result = conn.execute(stmt).fetchall()
        return [dict(row) for row in result]

    @staticmethod
    def update(hacker_id, name=None, email=None, password=None):
        """Update hacker details."""
        values = {}
        if name:
            values['name'] = name
        if email:
            values['email'] = email
        if password:
            values['password'] = generate_password_hash(password)
        if values:
            stmt = HackerTable.update().where(HackerTable.c.id == hacker_id).values(values)
            with engine.connect() as conn:
                conn.execute(stmt)
            return f"Hacker {hacker_id} updated successfully."
        return "No updates provided."

    @staticmethod
    def delete(hacker_id):
        """Delete a hacker."""
        stmt = HackerTable.delete().where(HackerTable.c.id == hacker_id)
        with engine.connect() as conn:
            conn.execute(stmt)
        return f"Hacker {hacker_id} deleted successfully."

class Malware:
    
    'table_name' = 'Malware'
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
    
    'table_name' = 'Data'
    data_id = Column(String, primary_key=True)
    content = Column(String(255))
    source = Column(String(255))
    
    instances = relationship('InstanceData',back_populates='Data')
    def create():
        pass
    
    def read():
        pass
    
    def update():
        pass
    
    def delete():
        pass

class InstanceData():
    
    'table_name' = 'InstanceData'

    malware_id = Column(String, ForeignKey('malware.instance_id'),)
    data_id = Column(String, ForeignKey('data.data_id'))

    malware = relationship("Malware", back_populates="instances")
    data = relationship("Data", back_populates="instances")


    
Session = sessionmaker(bind=engine)
session = Session()
metadata.create_all(engine)

session.add_all()
session.commit()


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



print('enter the attributes of the hacker')
name = input('name: ')
email = input('email: ')
password = input('password: ')
id = input('id: ')
Hacker_ins = Hacker.insert().values(name=name, email=email,password=password,id=id)
print(str(Hacker_ins))
session.execute(Hacker_ins)
session.commit()
result = session.execute(select(Hacker))
for row in result:
    print(row)
result = session.execute(select(Hacker).where(Hacker.c.id == '1'))
for row in result:
    print(row)
    
try:
   
    session.commit()
except Exception as e:
    print(f"An error occurred: {e}")
session.commit()

def create():
    pass

def read():
    pass

def update():
    pass

def delete():
    pass


