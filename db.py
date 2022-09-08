from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# connect with database
engine = create_engine('sqlite:///test.sqlite', echo=True)
# manage tables
base = declarative_base()

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('login', String(200), nullable=False),
             Column('password', String(200), nullable=False),
             # Column('created_on', DateTime(), default=datetime.now),
             # Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
             )

token = Table('token', metadata,
              Column('token', String(200), default='oifgifhgmlfjg'),
              Column('login', ForeignKey('user.login'))
              )

messages = Table('messages', metadata,
                 Column('login', ForeignKey('user.login')),
                 #   Column('created_on', DateTime(), default=datetime.now),
                 Column('message', Text(), nullable=False)
                 )
metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
result = session.query(user).all()
for row in result:
    print(row.login, row.password)
