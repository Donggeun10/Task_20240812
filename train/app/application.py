import logging
import sys
import time
from contextlib import asynccontextmanager

from fastapi import (FastAPI, Depends, Request)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from train.app import crud, database
from train.app.configuration.FlatbuffersMessageConverter import (
    FlatBuffersRoute)
from train.app.configuration.LoggingConfig import stream_handler, \
    file_handler
from train.app.configuration.SecurityConfig import verification
from train.app.controller import TrackingMemberController, InitController
from train.app.database import get_db
from train.app.schema.Item import ItemCreate

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
app.include_router(TrackingMemberController.router)
app.include_router(InitController.router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 1000)
    response.headers["X-Process-Time-ms"] = str(process_time)

    return response




app.router.route_class = FlatBuffersRoute



@app.get("/")
async def root(authentication = Depends(verification)):
    print(authentication)
    return RedirectResponse(url="/app-console-tracking-members")


@app.get("/items")
async def get_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.post("/item")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item)
    return db_item

import uvicorn

def serve(args):
    uvicorn.run(app, host="0.0.0.0", port=int(args[2]),
                reload=False,
                workers=1)

if __name__ == "__main__":
    serve(sys.argv)