import sqlalchemy.sql.sqltypes
from sqlalchemy import Column, String, PrimaryKeyConstraint, func

from test.train.app.database import Base


class app_tracking_member(Base):
  __tablename__ = "tb_app_tracking_member"
  game_code = Column(String(20))
  device_os = Column(String(20))
  user_id = Column(String(45))
  insert_timestamp = Column(sqlalchemy.DateTime, server_default=func.now())
  use_yn = Column(String(1) , default='Y')

  __table_args__ = (
    PrimaryKeyConstraint(game_code, device_os, user_id),
    {},
  )