

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from train.app import crud
from train.app.configuration.WebConfig import application_vnd

from train.app.database import get_db
from train.app.domain.CrashReportMessage import InitMessage
from train.app.entity.App import App
from train.app.service import AppService, InitService
from train.app.service.GcpPublisher import publish_message

router = APIRouter(
    prefix="/api/v1",
    tags=["init"],
)

@router.post("/init", dependencies=[Depends(application_vnd)])
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