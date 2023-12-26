from sqlalchemy.orm import Session

from models import MemberModel
from schemas.member_schema import *
from crud.members_crud import *


def add_solo_artist(db: Session, artist_data: SoloArtistCreate):
	artist = MemberModel(**artist_data.model_dump())
	artist.solo = True
	db.add(artist)
	db.commit()
	db.refresh(artist)
	return artist


def get_solo_artists(db: Session, skip: int = 0, limit: int = 10):
    return db.query(MemberModel).where(MemberModel.solo == True).offset(skip).limit(limit).all()


def get_solo_artist(db: Session, artist_id: int):
	return get_member(db, artist_id)


def update_solo_artist(db: Session, artist_id: int, new_artist: dict):
	return update_member(db, artist_id, new_artist)


def delete_solo_artist(db: Session, artist_id: int):
	return delete_member(db, artist_id)