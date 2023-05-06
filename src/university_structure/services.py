from abc import ABC
from src.university_structure.schemas import (
    InFaculty, OutFaculty,
    InSpecialization, OutSpecialization,
    InProfession, OutProfession
)
from src.university_structure.models import Faculty, Specialization, Profession, SpecializationProfession
from sqlalchemy import select, distinct, and_
from sqlalchemy.ext.asyncio import AsyncSession


class EntityService(ABC):
    @staticmethod
    async def _get_list(session: AsyncSession, model_class: any) -> list:
        query = select(model_class)
        cursor = await session.execute(query)
        rows = [row[0] for row in cursor.all()]
        return rows

    @staticmethod
    async def _create(session: AsyncSession, model_class: any, data: dict) -> any:
        new_entity = model_class(**data)
        session.add(new_entity)
        await session.commit()
        return new_entity


class FacultyService(EntityService):
    __MODEL_CLASS = Faculty
    __IN_SCHEMA_CLASS = InFaculty
    __OUT_SCHEMA_CLASS = OutFaculty

    @classmethod
    async def get_faculties(cls, session: AsyncSession) -> list[OutFaculty]:
        rows = await super()._get_list(session, cls.__MODEL_CLASS)
        return [cls.__OUT_SCHEMA_CLASS(id=row.id, name=row.name) for row in rows]

    @classmethod
    async def create_faculty(cls, session: AsyncSession, faculty: InFaculty) -> None:
        await super()._create(session, cls.__MODEL_CLASS, faculty.dict())


class SpecializationService(EntityService):
    __MODEL_CLASS = Specialization
    __IN_SCHEMA_CLASS = InSpecialization
    __OUT_SCHEMA_CLASS = OutSpecialization

    @classmethod
    async def get_specializations_by_faculty(cls, session: AsyncSession, faculty_id: int) -> list[OutSpecialization]:
        query = select(cls.__MODEL_CLASS).where(cls.__MODEL_CLASS.faculty_id == faculty_id)
        cursor = await session.execute(query)
        rows = [row[0] for row in cursor.all()]
        return [cls.__OUT_SCHEMA_CLASS(id=row.id, name=row.name) for row in rows]

    @classmethod
    async def create_specialization(cls, session: AsyncSession, specialization: InSpecialization) -> None:
        await super()._create(session, cls.__MODEL_CLASS, specialization.dict())


class ProfessionService(EntityService):
    __MODEL_CLASS = Profession
    __IN_SCHEMA_CLASS = InProfession
    __OUT_SCHEMA_CLASS = OutProfession

    @classmethod
    async def get_professions_by_specialization(cls, session: AsyncSession, specialization_id: int) -> list[OutSpecialization]:
        query = select(Profession).join(SpecializationProfession).\
            where(
                and_(
                    Profession.id == SpecializationProfession.profession_id,
                    SpecializationProfession.specialization_id == specialization_id
                )
        )
        cursor = await session.execute(query)
        rows = [row[0] for row in cursor.all()]
        return [cls.__OUT_SCHEMA_CLASS(id=row.id, name=row.name) for row in rows]

    @classmethod
    async def create_profession(cls, session: AsyncSession, profession: InProfession) -> None:
        query = select(Profession).where(Profession.name == profession.name)
        cursor = await session.execute(query)
        new_profession = cursor.first()[0]
        if not new_profession:
            new_profession = await super()._create(session, cls.__MODEL_CLASS, dict(name=profession.name))
            await session.refresh(new_profession)

        try:
            for specialization_id in profession.specializations:
                new_sp = SpecializationProfession(specialization_id=specialization_id, profession_id=new_profession.id)
                session.add(new_sp)
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise ex
