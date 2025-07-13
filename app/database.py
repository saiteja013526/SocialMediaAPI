import time
import psycopg2
from sqlalchemy import create_engine;
from psycopg2.extras import RealDictCursor;
from sqlalchemy.ext.declarative import declarative_base;
from sqlalchemy.orm import sessionmaker 


import urllib.parse

encoded_password = urllib.parse.quote("dell@123")
#print(encoded_password)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dell%40123@localhost/fastapi"


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


while True:
    try:
        connection = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='dell@123' )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print("Connected to database successfully!")
        break
    except Exception as error:
        print("connection to Database failed")
        print("error: ",error)
        time.sleep(3)   
