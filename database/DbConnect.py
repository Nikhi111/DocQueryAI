
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine=create_engine(db_url, pool_pre_ping=True, pool_recycle=300, connect_args={"sslmode": "require"} )
Sessionlocal=sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine)
Base = declarative_base()
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
