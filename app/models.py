
from .database import Base

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
  __tablename__ = "posts"

  id = Column( Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default='TRUE', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # Foreign key relation.
 
  owner = relationship("Users")
  

class Users(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String(18), nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String(128), nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  