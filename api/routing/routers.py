from api.services.services import news_service
from fastapi import APIRouter, Query
from api.schemas.schemas import news_schema

router = APIRouter()


@router.get('/news', response_model=news_schema)
def news_router(limit: Query(50, ge=1, le=1000),
                page: Query(1, ge=1)):
    return news_service(limit=limit, page=page)