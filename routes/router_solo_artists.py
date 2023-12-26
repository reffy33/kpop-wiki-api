from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.member_schema import *
from crud.solo_artists_crud import *


router_solo_artists = APIRouter(prefix='/solo_artists', tags=['Solo Artists'])


@router_solo_artists.get("/", response_model=List[ArtistSchema])
async def read_solo_artists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_solo_artists(db, skip=skip, limit=limit)


@router_solo_artists.get("/{artist_id}", response_model=ArtistSchema)
async def read_solo_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = get_solo_artist(db, artist_id)
    if not artist is None:
        return artist
    raise HTTPException(status_code=404, detail="Artist not found")


@router_solo_artists.post("/")
async def create_solo_artist(artist_data: SoloArtistCreate, db: Session = Depends(get_db)):
    artist = add_solo_artist(db, artist_data)
    return artist


@router_solo_artists.patch("/{artist_id}")
async def update_solo_artist_route(artist_id: int, artist_data: MemberUpdate, db: Session = Depends(get_db)):
    artist_data.solo = True
    new_artist = update_solo_artist(db, artist_id, artist_data.model_dump())
    if new_artist:
        return new_artist
    raise HTTPException(status_code=404, detail="Artist not found")


@router_solo_artists.delete("/{artist_id}")
async def delete_member_route(artist_id: int, db: Session = Depends(get_db)):
    member = delete_member(db, artist_id)
    if member:
        return {"message": "Member deleted"}
    raise HTTPException(status_code=404, detail="Member not found")



