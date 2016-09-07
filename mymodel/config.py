from mymodel import *
from mymodel import Base

def create_tables(engine):
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)
