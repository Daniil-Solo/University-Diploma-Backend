from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specializations = relationship("Specialization")


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))


specialization_profession = Table(
    "specialization_profession",
    Base.metadata,
    Column("specialization_id", ForeignKey("specializations.id")),
    Column("professions_id", ForeignKey("professions.id")),
)


class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
