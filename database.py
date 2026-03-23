from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.vbccfnvvmsmhvelozhcc:hk9.%2Abnd2.-T%267b@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # important for Supabase
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
