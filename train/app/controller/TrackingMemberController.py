from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from train.app.configuration.SecurityConfig import verification
from train.app.configuration.database import get_db
from train.app.schema.App_tracking_member import app_tracking_member_create
from train.app.service import crud

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

@router.post("/app-tracking-member",
             status_code=status.HTTP_201_CREATED,
             responses={
                201: {
                    "content": {"application/json": {}},
                    "description": "member is properly inserted",
                }
})
async def app_tracking_member(member: app_tracking_member_create, db: Session = Depends(get_db)):
    stored_member = crud.save_app_tracking_member(db, member)
    if stored_member is None:
        raise HTTPException(status_code=500, detail="member("+member.user_id+") is not properly inserted")

    return {"result":"member("+stored_member.user_id+") is properly inserted"}

@router.put("/app-tracking-members/{user_id}",
            status_code = status.HTTP_202_ACCEPTED,
            responses={
                202: {
                    "content": {"application/json": {}},
                    "description": "member is properly updated",
                }
})
async def get_app_tracking_member(user_id: str, member: app_tracking_member_create,  db: Session = Depends(get_db)):
    member = crud.update_app_tracking_member(db, user_id, member)
    if member is None:
        raise HTTPException(status_code=404, detail="member not found")

    return member

@router.delete("/app-tracking-members/{user_id}",
               status_code=status.HTTP_202_ACCEPTED,
               responses={
                   202: {
                       "content": {"application/json": {}},
                       "description": "member is properly deleted",
                   }
})
async def delete_app_tracking_member(user_id: str, db: Session = Depends(get_db)):
    crud.delete_app_tracking_member(db, user_id)

    return {"result":"member("+user_id+") is properly deleted"}
