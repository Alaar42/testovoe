from sqlalchemy.orm import sessionmaker
from db import engine, user, token
Session = sessionmaker(bind=engine)
session = Session()
result = session.query(user, token).join(token).all()
#print(result)
for row in result:
    print(row.login, row.password, row.token)
