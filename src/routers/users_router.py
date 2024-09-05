from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.controller import users_controller
from src.schemas.users_schema import UserCreate, UserResponse, PaginatedUserResponse
from src.utils.logger import get_logger

log = get_logger(__name__)

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse)
def post_users(req: UserCreate, db: Session = Depends(get_db)):
    log.info(f"post_users - {req.user_id}")
    return users_controller.register_user(req, db)


@router.get("/{user_id}", response_model=UserResponse)
def get_one_user(user_id: str, db: Session = Depends(get_db)):
    log.info(f"user_id: {user_id}")
    return users_controller.find_user(user_id, db)


# @router.get("", response_model=list[UserResponse])
# def get_all_users(db: Session = Depends(get_db)):
#     return users_controller.find_all_users(db)

@router.get("", response_model=PaginatedUserResponse)
def get_all_users(offset: int = 0,
                  limit: int = 10,
                  fromDateTime: Optional[datetime] = None,
                  toDateTime: Optional[datetime] = None,
                  db: Session = Depends(get_db)
                  ):
    return users_controller.find_all_users(db, offset, limit, fromDateTime, toDateTime)


# headers = {"X-Custom-Header": "Custom value"}
# return JSONResponse(status_code=200, content={"message": "Custom headers"}, headers=headers)

#  return JSONResponse(status_code=400, content={"message": "Bad Request"})

# raise HTTPException(status_code=400, detail="This is a bad request")
