import logging
from functools import lru_cache

from sqlalchemy.orm import Session

from test.train.app.configuration.LoggingConfig import stream_handler, file_handler
from test.train.app.entity.App import App
from test.train.app.entity.App_tracking_member import app_tracking_member
from test.train.app.entity.Item import Item
from test.train.app.schema.App_tracking_member import app_tracking_member_create
from test.train.app.schema.Item import ItemCreate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def get_items(db: Session):
  return db.query(Item).all()

def get_item(db: Session, item_id: int):
  return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate):
  db_item = Item(**item.model_dump())
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

def update_item(db: Session, item: Item, updated_item: ItemCreate):
  for key, value in updated_item.model_dump().items():
    setattr(item, key, value)
  db.commit()
  db.refresh(item)
  return item

def delete_item(db: Session, item: Item):
  db.delete(item)
  db.commit()

def get_app_tracking_members(db: Session):
  query = db.query(app_tracking_member)
  logger.debug(query)
  return query.all()

def get_app_tracking_member(db: Session, user_key: str):
  query = db.query(app_tracking_member).filter(app_tracking_member.user_id == user_key)
  logger.debug(query)
  return query.all()

def save_app_tracking_member(db: Session, member: app_tracking_member_create):
  member_dict = member.model_dump()
  new_member =  app_tracking_member(**member_dict)
  db.add(new_member)
  db.commit()
  db.refresh(new_member)
  return new_member

db : Session
def set_db_session(db_session : Session):
  global db
  db = db_session

@lru_cache()
def get_app(game_code : str, device_os : str):
  query = db.query(App).filter(App.game_code == game_code, App.device_os == device_os)
  # logger.debug(query)
  return query.first()