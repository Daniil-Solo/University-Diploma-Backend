from sqlalchemy import Column, Integer, String, JSON

from src.base import Base


class Elective(Base):
    __tablename__ = "electives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Integer, nullable=False)
    vector = Column(JSON, nullable=False)
