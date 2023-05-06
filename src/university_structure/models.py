from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from src.base import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    specializations = relationship("Specialization")


specialization_profession = Table(
    "specialization_profession",
    Base.metadata,
    Column("specialization_id", ForeignKey("specializations.id"), nullable=False),
    Column("professions_id", ForeignKey("professions.id"), nullable=False),
    UniqueConstraint("specialization_id", "professions_id")
)


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    professions = relationship(
        "Profession", secondary=specialization_profession, back_populates="specializations"
    )
    __table_args__ = (
        UniqueConstraint("faculty_id", "name"),
    )


class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    specializations = relationship(
        "Specialization", secondary=specialization_profession, back_populates="professions"
    )
