import json
from sqlalchemy.ext.asyncio import AsyncSession
from config import PROFESSIONS_FILENAME, ELECTIVES_FILENAME

from university_structure.services import (
    FacultyService, SpecializationService, ProfessionService
)
from ranking_of_electives.services import ElectiveService
from university_structure.schemas import (
    InFaculty, InSpecialization, InAdminProfession
)
from ranking_of_electives.schemas import InAdminElective


class DataBaseInitService:
    @staticmethod
    async def init_db(session: AsyncSession) -> None:
        mm_faculty = await FacultyService.create_faculty(session, InFaculty(name="Механико-математический"))
        ec_faculty = await FacultyService.create_faculty(session, InFaculty(name="Экономический"))
        fz_faculty = await FacultyService.create_faculty(session, InFaculty(name="Физический"))

        pmi_mm_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Прикладная математика и информатика", faculty_id=mm_faculty.value)
        )
        kmb_mm_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Компьютерная безопасность", faculty_id=mm_faculty.value)
        )
        pmi_ec_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Прикладная математика и информатика", faculty_id=ec_faculty.value)
        )
        mg_ec_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Менеджмент", faculty_id=ec_faculty.value)
        )
        pmi_fz_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Прикладная математика и информатика", faculty_id=fz_faculty.value)
        )
        rf_fz_specialization = await SpecializationService.create_specialization(
            session, InSpecialization(name="Радиофизика", faculty_id=fz_faculty.value)
        )

        with open(ELECTIVES_FILENAME, "r", encoding='utf-8') as f:
            electives = json.load(f)
        for elective in electives:
            await ElectiveService.create_elective(
                session,
                InAdminElective(
                    id=elective['id'],
                    name=elective['name'],
                    type=elective['type'],
                    vector=elective['data']
                )
            )
        del electives

        with open(PROFESSIONS_FILENAME, "r", encoding='utf-8') as f:
            professions = json.load(f)

        pmi_professions = {6, 1, 9, 10, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
        mg_professions = {1, 2, 3, 4, 5, 6, 7, 8}
        rf_professions = {21, 22, 23, 24, 19}
        kmb_professions = {12, 10, 14, 18, 19, 16, 25}

        for profession in professions:
            specializations = []
            if profession['id'] in pmi_professions:
                specializations.append(pmi_fz_specialization.value)
                specializations.append(pmi_ec_specialization.value)
                specializations.append(pmi_mm_specialization.value)
            if profession['id'] in mg_professions:
                specializations.append(mg_ec_specialization.value)
            if profession['id'] in rf_professions:
                specializations.append(rf_fz_specialization.value)
            if profession['id'] in kmb_professions:
                specializations.append(kmb_mm_specialization.value)
            await ProfessionService.create_profession(
                session,
                InAdminProfession(
                    id=profession['id'],
                    name=profession['name'],
                    vector=profession['data'],
                    specializations=specializations
                )
            )
