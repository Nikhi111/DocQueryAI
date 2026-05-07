from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url="postgresql://neondb_owner:npg_9wbOg4cVimqv@ep-old-moon-a7kmc45j-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
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
