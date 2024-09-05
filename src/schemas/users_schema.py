from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_password: str


class UserResponse(BaseModel):
    user_id: str
    user_name: str | None = None
    created_date_time: datetime | None = None
    modified_date_time: datetime | None = None

    class Config:
        # v1 style
        # orm_mode = True
        # v2 style
        from_attributes = True

        # JSON 직렬화 시 ISO 8601 포맷으로 변환
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        }


class PaginatedUserResponse(BaseModel):
    offset: int
    limit: int
    allCounts: int
    pageCounts: int
    items: List[UserResponse]  # 여기에 UserResponse의 리스트가 포함됨
