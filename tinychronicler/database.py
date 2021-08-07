import databases
import sqlalchemy

from tinychronicler.constants import DATABASE_URL

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Define tables
compositions = sqlalchemy.Table(
    "compositions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
)

# Create tables
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
