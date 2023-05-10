from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.admin.services import DataBaseInitService


router = APIRouter(prefix="/admin")


@router.get(
    "/init_db",
    description="Заполняет базу данных тестовыми данными",
    tags=["Администрирование"]
)
async def create_profession(session: AsyncSession = Depends(get_async_session)):
    try:
        await DataBaseInitService.init_db(session)
        return {
            "message": "Операции успешно выполнены!"
        }
    except Exception as ex:
        print(ex)
        return {
            "message": "Что-то пошло не так!"
        }
