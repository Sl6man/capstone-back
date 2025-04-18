# data/db_config.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create Base class first


# Create engine



## engine = create_engine("postgresql://postgres:your_password@localhost:5432/snap_scope") # for sultan

engine = create_engine("postgresql://postgres:1234@localhost/snap_scope")    # for khaled



# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

