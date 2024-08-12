from pydantic import BaseModel

class app_base(BaseModel):
    game_code : str
    device_os : str
    display_name : str
    package_name : str

class app_create(app_base):
    pass

class app(app_base):

    class Config:
        orm_mode = True