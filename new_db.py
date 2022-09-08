from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from db import engine, user, token
test = 'qwetr'
Session = sessionmaker(bind=engine)
session = Session()
#result = session.query(user).all()
# print(result)
# stmt = insert(user).values(
#     login='token',
#     password='dfgdfgdf'
# )
# compiled = stmt.compile()
with engine.connect() as conn:
    result = conn.execute(
        insert(user),
        [
            {"login": test, "password": "Sandy Cheeks"},
            {"login": "patrick", "password": "Patrick Star"}
        ]
    )
#result.inserted_primary_key
