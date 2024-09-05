# from sqlalchemy import Column, String
#
# from src.config.database import Base
#
#
# class User(Base):
#     __tablename__ = "tb_user"
#
#     user_id = Column(String, primary_key=True, index=True)
#     user_name = Column(String, index=True)
#     user_password = Column(String, index=True)
#     created_date_time
from datetime import datetime

from sqlalchemy import Column, String, DateTime, func, event

from src.config.database import Base


class User(Base):
    __tablename__ = "tb_user"

    user_id = Column(String(255), primary_key=True, index=True)
    user_name = Column(String(255), nullable=True)
    user_password = Column(String(255), nullable=True)
    created_date_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_date_time = Column(DateTime(timezone=True), onupdate=func.now())


# 이벤트 리스너 정의: before_insert와 before_update 시점에 자동으로 시간 설정
@event.listens_for(User, 'before_insert')
def set_created_date_time(mapper, connection, target):
    if not target.created_date_time:
        target.created_date_time = datetime.utcnow()


@event.listens_for(User, 'before_update')
def set_modified_date_time(mapper, connection, target):
    target.modified_date_time = datetime.utcnow()
