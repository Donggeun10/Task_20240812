from pydantic import BaseModel

class app_tracking_member_base(BaseModel):
  game_code : str
  device_os : str
  user_id : str

class app_tracking_member_create(app_tracking_member_base):
  pass

class app_tracking_member(app_tracking_member_base):

  class Config:
    orm_mode = True