from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.university_structure.services import FacultyService, SpecializationService, ProfessionService
from src.university_structure.schemas import (
    OutFaculty, OutSpecialization, OutProfession
)
from src.database import get_async_session

router = APIRouter(prefix="/structure")


@router.get(
    "/faculties",
    response_model=list[OutFaculty],
    description="Возвращает все факультеты",
    tags=["Факультет"]
)
async def get_faculties(session: AsyncSession = Depends(get_async_session)):
    try:
        return await FacultyService.get_faculties(session)
    except Exception as ex:
        print(ex)
        return {
            "message": "Что-то пошло не так!"
        }


@router.get(
    "/specializations",
    response_model=list[OutSpecialization],
    description="Возвращает направления по факультету",
    tags=["Направление"]
)
async def get_specializations(faculty_id: int = Query(), session: AsyncSession = Depends(get_async_session)):
    try:
        return await SpecializationService.get_specializations_by_faculty(session, faculty_id)
    except Exception as ex:
        print(ex)
        return {
            "message": "Что-то пошло не так!"
        }


@router.get(
    "/professions",
    response_model=list[OutProfession],
    description="Возвращает профессии по направлению",
    tags=["Профессия"]
)
async def get_professions(specialization_id: int = Query(), session: AsyncSession = Depends(get_async_session)):
    try:
        return await ProfessionService.get_professions_by_specialization(session, specialization_id)
    except Exception as ex:
        print(ex)
        return {
            "message": "Что-то пошло не так!"
        }
