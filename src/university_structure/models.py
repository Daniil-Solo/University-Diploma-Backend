from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, JSON
from sqlalchemy.orm import relationship

from base import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    specializations = relationship("Specialization")


class SpecializationProfession(Base):
    __tablename__ = "specialization_profession"

    specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=False)
    profession_id = Column(Integer, ForeignKey("professions.id"), nullable=False)
    __table_args__ = (
        UniqueConstraint("specialization_id", "profession_id"),
        PrimaryKeyConstraint("specialization_id", "profession_id"),
    )


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    __table_args__ = (
        UniqueConstraint("faculty_id", "name"),
    )


class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    vector = Column(JSON, nullable=False)
