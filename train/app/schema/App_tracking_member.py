from pydantic import BaseModel

class app_tracking_member_base(BaseModel):
    title_code : str
    market_os : str
    user_id : str

class app_tracking_member_create(app_tracking_member_base):

    def to_dict(self):
        return {
            "title_code" : self.title_code,
            "market_os" : self.market_os,
            "user_id" : self.user_id
        }

class app_tracking_member(app_tracking_member_base):

    class Config:
        orm_mode = True