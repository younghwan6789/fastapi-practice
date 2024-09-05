from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.users_model import User
from src.schemas.users_schema import UserCreate, UserResponse
from src.utils.logger import get_logger

log = get_logger(__name__)


def create_user(req: UserCreate, db: Session = Depends(get_db)):
    log.info(f"create_user - id: {req.user_id}, name: {req.user_name}, password: {req.user_password}")
    db_user = User(
        user_id=req.user_id,
        user_name=req.user_name,
        user_password=req.user_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        user_id=req.user_id,
        user_name=req.user_name
    )
    # return {"status": "ok"}


def find_user(user_id: str, db: Session = Depends(get_db)):
    log.info(f"find_user - {user_id}")
    return db.query(User).filter(User.user_id == user_id).first()


# def find_all_users(db: Session = Depends(get_db)):
#     log.info(f"find_all_users")
#     return db.query(User).offset(0).limit(10).all()


def find_all_users(db: Session, offset: int = 0, limit: int = 10, from_date: datetime = None, to_date: datetime = None):
    query = db.query(User)

    # 날짜 필터링 조건 추가
    if from_date:
        query = query.filter(User.created_date_time >= from_date)
    if to_date:
        query = query.filter(User.created_date_time <= to_date)

    # 전체 개수
    all_counts = query.count()

    # 페이징 적용 및 데이터 가져오기
    users = query.offset(offset).limit(limit).all()

    return {
        "all_counts": all_counts,
        "page_counts": len(users),
        "items": users
    }


# def update_user(db: Session, user_id: str, user_data: UserCreate):
#     db_user = db.query(User).filter(User.user_id == user_id).first()
#     if db_user:
#         db_user.user_name = user_data.user_name
#         db_user.user_password = user_data.user_password
#         db.commit()
#         db.refresh(db_user)
#     return db_user
#
# def delete_user(db: Session, user_id: str):
#     db_user = db.query(User).filter(User.user_id == user_id).first()
#     if db_user:
#         db.delete(db_user)
#         db.commit()
#     return db_user