from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from itertools import chain

from university_structure.models import Profession
from university_structure.services import EntityService
from .models import Elective
from .schemas import InAdminElective, ElectiveGroup, OutElective
from .utils import from_dict_to_sparse_array, calculate_similarity
from .constants import (
    ELECTIVE_GROUP_NAME_FOR_TYPE, ELECTIVES_FOR_SPECIALIZATION, ELECTIVE_COUNT
)


class ElectiveService(EntityService):
    __MODEL_CLASS = Elective
    __IN_SCHEMA_CLASS = InAdminElective
    __OUT_SCHEMA_CLASS = OutElective

    @classmethod
    async def create_elective(cls, session: AsyncSession, elective: InAdminElective) -> OutElective:
        elective = await super()._create(session, cls.__MODEL_CLASS, elective.dict())
        return OutElective(id=elective.id, title=elective.name)


class RankingOfElectivesService:
    @staticmethod
    async def get_available_electives_by_specialization(s: AsyncSession, specialization_id: int) -> dict[str:list[int]]:
        available_electives = ELECTIVES_FOR_SPECIALIZATION[specialization_id]
        unique_electives = dict()
        all_elective_id_set = set(chain.from_iterable(available_electives.values()))
        for group_name in available_electives.keys():
            elective_id_set = set(available_electives[group_name])
            unique_electives[group_name] = list(elective_id_set & all_elective_id_set)
            all_elective_id_set = all_elective_id_set - elective_id_set
        return unique_electives

    @staticmethod
    async def get_relevant_electives_by_profession(
            session: AsyncSession, elective_dict_groups: dict[str:list[int]], profession_id: int) -> list[ElectiveGroup]:

        elective_id_list = list(chain.from_iterable(elective_dict_groups.values()))
        elective_query = select(Elective).where(Elective.id.in_(elective_id_list))
        elective_records = await session.execute(elective_query)
        elective_records = [el[0] for el in elective_records.all()]

        profession_query = select(Profession).where(Profession.id == profession_id)
        profession_record = await session.execute(profession_query)
        profession_record = profession_record.first()[0]
        profession_sparse_array = from_dict_to_sparse_array(profession_record.vector)

        electives = []
        for elective_record in elective_records:
            elective_sparse_array = from_dict_to_sparse_array(elective_record.vector)
            similarity = calculate_similarity(profession_sparse_array, elective_sparse_array)
            electives.append((elective_record, similarity))

        elective_groups = []
        for elective_type in ELECTIVE_GROUP_NAME_FOR_TYPE:
            items = []
            group_name = ELECTIVE_GROUP_NAME_FOR_TYPE[elective_type]
            elective_name_set = set()
            elective_name_set_add = elective_name_set.add
            filtered_electives = [
                el for el in electives
                if el[0].id in elective_dict_groups[group_name] and not (el in elective_name_set or elective_name_set_add(el))
            ]
            for (elective_record, _) in sorted(filtered_electives, key=lambda x: x[1], reverse=True)[:ELECTIVE_COUNT]:
                items.append(OutElective(id=elective_record.id, title=elective_record.name))
            elective_groups.append(ElectiveGroup(name=group_name, items=items))

        return elective_groups
