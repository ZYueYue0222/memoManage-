from sqlalchemy import ForeignKey, Integer,Column,String
from app.get_db import Base

class Memo(Base):
    __tablename__="memo"
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(50),nullable=False)
    content=Column(String(100),nullable=False)
    