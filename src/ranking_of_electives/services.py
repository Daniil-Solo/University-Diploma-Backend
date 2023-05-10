from sqlalchemy.ext.asyncio import AsyncSession

from src.ranking_of_electives.schemas import InAdminElective, OutElective
from src.ranking_of_electives.models import Elective
from src.university_structure.services import EntityService


class ElectiveService(EntityService):
    __MODEL_CLASS = Elective
    __IN_SCHEMA_CLASS = InAdminElective
    __OUT_SCHEMA_CLASS = OutElective

    @classmethod
    async def create_elective(cls, session: AsyncSession, elective: InAdminElective) -> OutElective:
        elective = await super()._create(session, cls.__MODEL_CLASS, elective.dict())
        return OutElective(id=elective.id, title=elective.name)

