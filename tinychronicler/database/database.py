import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from tinychronicler.constants import DATABASE_URL

# Declare our database handler, this one will execute all queries
database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
