from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.members_crud import *
from schemas.member_schema import *

from routes.websocket import send_broadcast


router_members = APIRouter(prefix='/members', tags=['Members'])


@router_members.get("/group_members/{group_id}", response_model=List[MemberSchema])
async def read_group_members(group_id: int, db: Session = Depends(get_db)):
    return get_group_members(db, group_id)


@router_members.get("/{member_id}", response_model=MemberSchema)
async def read_member(member_id: int, db: Session = Depends(get_db)):
    member = get_member(db, member_id)

    if member.group_id is None:
        raise HTTPException(status_code=404, detail="This is a solo artist")

    if not member is None:
        return member
    
    raise HTTPException(status_code=404, detail="Member not found")


@router_members.post("/{group_id}", response_model=MemberSchema)
async def create_member(group_id: int, member_data: MemberCreate, db: Session = Depends(get_db)):
    member = add_member(db, group_id, member_data)
    await send_broadcast(f"New member {member.stage_name} was added to the group {member.group.name}")
    return member

@router_members.post("/add_members/{group_id}")
async def create_members(group_id: int, members_data: List[MemberCreate], db: Session = Depends(get_db)):
    new_members = add_members(db, group_id, members_data)
    await send_broadcast(f"{len(new_members)} new members was added to the group {new_members[0].group.name}")
    return new_members


@router_members.patch("/{member_id}", response_model=MemberSchema)
async def update_member_route(member_id: int, member_data: MemberUpdate, db: Session = Depends(get_db)):
    new_member = update_member(db, member_id, member_data.model_dump())
    if new_member:
        await send_broadcast(f"The member {new_member.stage_name} was updated")
        return new_member
    raise HTTPException(status_code=404, detail="Member not found")


@router_members.delete("/{member_id}")
async def delete_member_route(member_id: int, db: Session = Depends(get_db)):
    member = delete_member(db, member_id)
    if member:
        await send_broadcast(f"The member {member.stage_name} was deleted")
        return {"message": "Member deleted"}
    raise HTTPException(status_code=404, detail="Member not found")
