import logging
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.orm import Session

from train.app.configuration.LoggingConfig import stream_handler, file_handler
from train.app.entity.App import App
from train.app.entity.App_tracking_member import app_tracking_member
from train.app.entity.Item import Item
from train.app.schema.App_tracking_member import app_tracking_member_create
from train.app.schema.Item import ItemCreate

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
    #logger.debug(query)
    return query.all()

def get_app_tracking_member(db: Session, user_key: str):
    query = db.query(app_tracking_member).filter(app_tracking_member.user_id == user_key)
    #logger.debug(query)
    return query.first()

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
    query = db.query(App).filter(App.title_code == game_code, App.market_os == device_os)
    # logger.debug(query)
    return query.first()

def update_app_tracking_member(db: Session, user_id : str, member_info : app_tracking_member_create):
    # Step 1: Retrieve the existing member and lock the row for update
    member = db.execute(
        select(app_tracking_member).filter(app_tracking_member.user_id == user_id).with_for_update()
    ).scalar_one_or_none()

    if member is None:
        return None

    # Step 3: Update the member's attributes
    for key, value in member_info.model_dump().items():
        setattr(member, key, value)

    # Step 4: Commit the changes to the database
    db.commit()

    # Step 5: Refresh the member instance
    db.refresh(member)

    return member

def delete_app_tracking_member(db: Session, user_id: str):
    query = db.query(app_tracking_member).filter(app_tracking_member.user_id
                                                 == user_id)
    #logger.debug(query)
    query.delete()
    db.commit()