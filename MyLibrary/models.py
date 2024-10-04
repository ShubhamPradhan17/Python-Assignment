import os
import bcrypt
from sqlobject import SQLObject, StringCol, IntCol, DateTimeCol, ForeignKey, BoolCol, FloatCol, connectionForURI, sqlhub
from dotenv import load_dotenv


load_dotenv()
db_path = os.path.abspath('my_library.db')
connection_string = f'sqlite:///{db_path}'
connection = connectionForURI(connection_string)
print(f"Database will be created at: {db_path}")
sqlhub.processConnection = connection

class Books(SQLObject):
    book_name = StringCol(notNone = False)
    author = StringCol(notNone = False)
    publisher = StringCol(notNone = False)
    quantity = IntCol(default = 0)
    issued_count = IntCol(default=0)
    genre = StringCol(notNone = False)
    isbn = StringCol(notNone = False)
    date_updated = DateTimeCol()

class Members(SQLObject):
    first_name = StringCol(notNone = False)
    last_name = StringCol(notNone = False)
    email = StringCol(notNone = False, unique=True)
    phone_no = StringCol(notNone = False)
    address = StringCol(notNone = False)
    debt = FloatCol(notNone = False)
    password = StringCol(notNone = False)
    role = StringCol(notNone = True, default="issuer")

class transactions(SQLObject):
    book = ForeignKey('Books', notNone=True)
    member = ForeignKey('Members', notNone=True)
    date_issued = DateTimeCol(default=DateTimeCol.now)
    due_date = DateTimeCol()
    date_submission = DateTimeCol(default=None)
    return_status = BoolCol(default=False)
    fine_amount = FloatCol(default=0.0)

    

# class Role(SQLObject):
#     role_name = StringCol(unique=True, notNone=True)

# class MemberRole(SQLObject):
#     members = ForeignKey('Members', notNone=True)
#     role = ForeignKey('Role', notNone=True)

def create_tables():
    # Create tables if they don't already exist
    Books.createTable(ifNotExists=True)
    Members.createTable(ifNotExists=True)
    transactions.createTable(ifNotExists=True)
    # Role.createTable(ifNotExists=True)
    # MemberRole.createTable(ifNotExists=True)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!")