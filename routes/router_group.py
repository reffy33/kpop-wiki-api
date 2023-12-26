from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.groups_crud import *
from schemas.group_schema import *
from schemas.group_type import GroupType


router_groups = APIRouter(prefix='/groups', tags=['Groups'])


@router_groups.get("/", response_model=List[GroupSchema])
async def read_groups(skip: int = 0, limit: int = 10, type: GroupType = None, db: Session = Depends(get_db)):
    return get_groups(db, skip=skip, limit=limit, type=type)


@router_groups.get("/{group_id}", response_model=GroupSchema)
async def read_group(group_id: int, db: Session = Depends(get_db)):
    group = get_group(db, group_id)
    if not group is None:
        return group
    raise HTTPException(status_code=404, detail="Group not found")


@router_groups.patch("/{group_id}", response_model=GroupSchema)
async def update_group_route(group_id: int, group_data: GroupUpdate, db: Session = Depends(get_db)):
    new_group = update_group(db, group_id, group_data.model_dump())
    if new_group:
        return new_group
    raise HTTPException(status_code=404, detail="Group not found")


@router_groups.post("/", response_model=GroupSchema)
async def create_group(group_data: GroupCreate, db: Session = Depends(get_db)):
    group = add_group(db, group_data)
    return group


@router_groups.delete("/{group_id}")
async def delete_group_route(group_id: int, db: Session = Depends(get_db)):
    result = delete_group(db, group_id)

    if result == "Group deleted":
        return {"message": result}
    
    if result == "Group not found":
        raise HTTPException(status_code=404, detail=result)
    
    if result == "Please delete non-solo members of the group first":
        raise HTTPException(status_code=422, detail=result)
    
    raise HTTPException(status_code=400)


@router_groups.delete("/force_delete/{group_id}")
async def delete_group_with_members_route(group_id: int, db: Session = Depends(get_db)):
    result = delete_group_with_members(db, group_id)
    
    if result == "Group deleted with non-solo members":
        return {"message": result}
    raise HTTPException(status_code=404, detail=result)
