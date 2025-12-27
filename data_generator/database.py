from sqlalchemy import create_engine
from config import DATABASE_URL
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL, echo=False)


Session = sessionmaker(bind=engine)
