from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql://root:adedara12@localhost:3306/books")
meta = MetaData()

Base = declarative_base()
SessionLocal= sessionmaker(bind=engine)