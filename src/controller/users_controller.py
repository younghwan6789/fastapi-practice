from datetime import datetime
from typing import Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.users_schema import UserCreate, UserResponse
from src.service import users_service
from src.utils.logger import get_logger

log = get_logger(__name__)


def register_user(req: UserCreate, db: Session = Depends(get_db)):
    return users_service.create_user(req, db)


def find_user(user_id: str, db: Session = Depends(get_db)):
    return users_service.find_user(user_id, db)


# def find_all_users(db: Session = Depends(get_db)):
#     return users_service.find_all_users(db)

def find_all_users(db: Session = Depends(get_db),
                   offset: int = Query(0, description="페이지 시작점"),
                   limit: int = Query(10, description="페이지 크기"),
                   fromDateTime: Optional[datetime] = Query(None, description="시작 날짜 필터"),
                   toDateTime: Optional[datetime] = Query(None, description="종료 날짜 필터")
                   ):
    result = users_service.find_all_users(
        db,
        offset=offset,
        limit=limit,
        from_date=fromDateTime,
        to_date=toDateTime
    )
    log.info("**********************")
    return {
        "offset": offset,
        "limit": limit,
        "allCounts": result["all_counts"],
        "pageCounts": result["page_counts"],
        "items": [UserResponse.from_orm(user) for user in result["items"]]
    }
