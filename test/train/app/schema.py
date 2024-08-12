from pydantic import BaseModel

class ItemBase(BaseModel):
  name: str
  description: str
  price: int

class ItemCreate(ItemBase):
  pass

class Item(ItemBase):
  id: int

  class Config:
    orm_mode = True

class app_console_tracking_member_base(BaseModel):
  game_code : str
  device_os : str
  user_id : str

class app_console_tracking_member_create(app_console_tracking_member_base):
  pass

class app_console_tracking_member(app_console_tracking_member_base):

  class Config:
    orm_mode = True