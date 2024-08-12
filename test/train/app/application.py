import logging
import time
from contextlib import asynccontextmanager

from fastapi import (FastAPI, HTTPException, Depends, Header, status, Request,
                     Response)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from test.train.app import crud, database
from test.train.app.configuration.FlatbuffersMessageConverter import (
    FlatBuffersRoute)
from test.train.app.configuration.LoggingConfig import stream_handler, \
    file_handler
from test.train.app.domain.CrashReportMessage import InitMessage
from test.train.app.entity.App import App
from test.train.app.schema.App_tracking_member import app_tracking_member_create
from test.train.app.schema.Item import ItemCreate
from test.train.app.service import AppService, InitService
from test.train.app.service.GcpPublisher import publish_message


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    database.create_tables()
    logger.info("Service started.")
    yield

    # When service is stopped.
    # shutdown()
    logger.info("Service stopped.")


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 1000)
    response.headers["X-Process-Time-ms"] = str(process_time)

    return response

def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/flatbuffers-v3 or application/flatbuffers-v4"""
    if {"application/flatbuffers-v3","application/flatbuffers-v4"}.issubset(content_type):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,f"Unsupported media type: {content_type}. It must be application/flatbuffers-v3,v4",)


app.router.route_class = FlatBuffersRoute

@app.post("/init", dependencies=[Depends(application_vnd)])
async def init(request: Request, response: Response, db: Session = Depends(get_db)):
    # logger.debug("appload processing will be started "+check_point)
    body : InitMessage = await request.body()
    game_code = body.game_code
    device_os = body.device_os
    # logger.debug(db)
    crud.set_db_session(db)
    app : App = crud.get_app(game_code, device_os)
    # logger.debug("data is loaded "+check_point)
    print(crud.get_app.cache_info())
    response.headers["Console-Tracking"] = "N"

    if(AppService.is_service_game_code(app)):
        if(InitService.is_sampled(app)):
            response.headers["Retry-When"] = "never"

        # publish message to gcp pubsub
        # logger.debug("it will be published "+check_point)
        publish_message(f"edge.appload.{body.version.name}", body)
    else:
        response.headers["Retry-When"] = "never"
        return "Game code not found"

    # logger.debug("appload is finished "+check_point)
    return "OK"

@app.get("/")
async def root():
    return RedirectResponse(url="/app-console-tracking-members")

@app.get("/app-tracking-members")
async def get_app_tracking_members(db: Session = Depends(get_db)):
    return crud.get_app_tracking_members(db)


@app.get("/app-tracking-members/{user_id}")
async def get_app_tracking_member(user_id: str, db: Session = Depends(get_db)):
    member = crud.get_app_tracking_member(db, user_id)
    if member is None:
        raise HTTPException(status_code=404, detail="member not found")
    return member

@app.post("/app-tracking-member")
async def app_tracking_member(member: app_tracking_member_create, db: Session = Depends(get_db)):
    return crud.save_app_tracking_member(db, member)


@app.get("/items")
async def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.post("/item")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item)
    return db_item

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, updated_item: schema.ItemCreate, db: Session = Depends(get_db)):
#   db_item = crud.get_item(db, item_id)
#   if db_item is None:
#     raise HTTPException(status_code=404, detail="Item not found")
#   updated_item = crud.update_item(db, db_item, updated_item)
#   return updated_item
#
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int, db: Session = Depends(get_db)):
#   db_item = crud.get_item(db, item_id)
#   if db_item is None:
#     raise HTTPException(status_code=404, detail="Item not found")
#   crud.delete_item(db, db_item)
#   return {"message": "Item deleted successfully"}

import uvicorn


def serve():
    uvicorn.run(app, host="0.0.0.0", port=9084,
                reload=False,
                workers=1)

if __name__ == "__main__":
    serve()