from sqlalchemy import create_engine, select, MetaData, Table, Column, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import sessionmaker


dbPath = 'trojan.db'
engine = create_engine('sqlite:///%s' % dbPath)
metadata = MetaData()

Hacker = Table(
    'Hacker', metadata,
    Column('id', String(60), primary_key=True),
    Column('name', String(60)),
    Column('email', String(60)),
    Column('password', String(255))
)

Malware = Table(
    'Malware', metadata,
    Column('instance_id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('status', Boolean)
)

Data = Table(
    'Data', metadata,
    Column('data_id', String, primary_key=True),
    Column('content', String(255)),
    Column('source', String(255))
)

InstanceData = Table(
    'InstanceData', metadata,
    Column('instance_id', String(60), ForeignKey('Malware.instance_id'), primary_key=True),
    Column('data_id', String(60), ForeignKey('Data.data_id'), primary_key=True)
)

Command = Table(
    'Command', metadata,
    Column('command_id', String, primary_key=True),
    Column('syntax', String(128)),
    Column('status', String(60)),
    Column('created_at', DateTime),
    Column('executed_at', DateTime)
)

MalwareCommand = Table(
    'MalwareCommand', metadata,
    Column('instance_id', String, ForeignKey('Malware.instance_id'), primary_key=True),
    Column('command_id', String, ForeignKey('Command.command_id'), primary_key=True)
)

Log = Table(
    'Log', metadata,
    Column('log_id', String, primary_key=True),
    Column('created_at', DateTime),
    Column('content', String(255))
)

Session = sessionmaker(bind=engine)
session = Session()
metadata.create_all(engine)
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
