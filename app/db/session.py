from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.globals import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
