#Used in all models
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["user","document"]

#Used in all models
Base = declarative_base()
