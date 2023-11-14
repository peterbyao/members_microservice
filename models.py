from sqlalchemy import Column, Integer, String, Float
from Resources.database import Base


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, index=True)
    member_name = Column(String, unique=True)
    portfolio_value = Column(Float)
    age = Column(Integer)
