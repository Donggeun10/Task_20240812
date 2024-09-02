import sqlalchemy.sql.sqltypes
from sqlalchemy import Column, String, PrimaryKeyConstraint, func

from train.app.configuration.database import Base


class app_tracking_member(Base):
  __tablename__ = "tb_app_tracking_member"
  title_code = Column(String(45))
  market_os = Column(String(45))
  user_id = Column(String(45))
  user_name = Column(String(45))
  insert_timestamp = Column(sqlalchemy.DateTime, server_default=func.now())
  use_yn = Column(String(1) , default='Y')

  __table_args__ = (
    PrimaryKeyConstraint(title_code, market_os, user_id),
    {},
  )