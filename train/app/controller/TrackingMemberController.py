from fastapi.params import Depends
from sqlalchemy.orm import Session

from starlette.responses import RedirectResponse

from train.app import crud

from train.app.configuration.SecurityConfig import verification
from fastapi import APIRouter, HTTPException

from train.app.database import get_db
from train.app.schema.App_tracking_member import app_tracking_member_create

router = APIRouter(
    prefix="",
    tags=["tracking-members"],
)

@router.get("/hello")
async def root(authentication = Depends(verification)):
    print(authentication)
    return RedirectResponse(url="/app-tracking-members")

@router.get("/app-tracking-members")
async def get_app_tracking_members(db: Session = Depends(get_db)):
    return crud.get_app_tracking_members(db)


@router.get("/app-tracking-members/{user_id}")
async def get_app_tracking_member(user_id: str, db: Session = Depends(get_db)):
    member = crud.get_app_tracking_member(db, user_id)
    if member is None:
        raise HTTPException(status_code=404, detail="member not found")
    return member

@router.post("/app-tracking-member")
async def app_tracking_member(member: app_tracking_member_create, db: Session = Depends(get_db)):
    return crud.save_app_tracking_member(db, member)