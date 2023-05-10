from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ranking_of_electives.services import RankingOfElectivesService


router = APIRouter(prefix="/ranking")


@router.get(
    "/get_electives",
    description="Возвращает ранжированные элективы",
    tags=["Ранжирование элективов"]
)
async def get_electives(specialization_id: int = Query(), profession_id: int = Query(),
                            session: AsyncSession = Depends(get_async_session)):
    electives = await RankingOfElectivesService.get_available_electives_by_specialization(session, specialization_id)
    return await RankingOfElectivesService.get_relevant_electives_by_profession(session, electives, profession_id)

