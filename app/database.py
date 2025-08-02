from sqlalchemy import create_engine;
from sqlalchemy.ext.declarative import declarative_base;
from sqlalchemy.orm import sessionmaker 
from .config import settings


import urllib.parse

encoded_password = urllib.parse.quote(settings.database_password)
#print(encoded_password)

# SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{encoded_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         connection = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='dell@123' )
#         cursor = connection.cursor(cursor_factory=RealDictCursor)
#         print("Connected to database successfully!")
#         break
#     except Exception as error:
#         print("connection to Database failed")
#         print("error: ",error)
#         time.sleep(3)   
