from abc import ABC
from src.university_structure.schemas import InFaculty, OutFaculty
from src.university_structure.models import Faculty
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class EntityService(ABC):
    @staticmethod
    async def _get_list(session: AsyncSession, model_class: any) -> list:
        query = select(model_class)
        cursor = await session.execute(query)
        rows = [row[0] for row in cursor.all()]
        return rows

    @staticmethod
    async def _create(session: AsyncSession, model_class: any, data: dict) -> None:
        new_entity = model_class(**data)
        session.add(new_entity)
        await session.commit()


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