from fastapi import Depends, Body
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.university_structure.services import FacultyService
from src.university_structure.schemas import OutFaculty, InFaculty
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


@router.post(
    "/faculties/create",
    description="Создает новый факультет",
    tags=["Факультет"]
)
async def create_faculty(faculty_data: InFaculty = Body(), session: AsyncSession = Depends(get_async_session)):
    try:
        await FacultyService.create_faculty(session, faculty_data)
        return {
            "message": "Факультет успешно создан!"
        }
    except Exception as ex:
        print(ex)
        return {
            "message": "Что-то пошло не так!"
        }
