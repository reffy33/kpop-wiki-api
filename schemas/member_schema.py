from pydantic import BaseModel
from typing import Optional
from datetime import date


class BaseMember(BaseModel):
    stage_name: str
    image_url: Optional[str] = None
    real_name: Optional[str] = None
    birthday: Optional[date] = None


class MemberCreate(BaseMember):
    position: Optional[str] = None
    ex_member: bool = False
    solo: bool = False
    solo_debut: Optional[date] = None


class SoloArtistCreate(BaseMember):
    solo_debut: date


class ArtistSchema(MemberCreate):
    id: int
    group_id: Optional[int] = None


class MemberSchema(MemberCreate):
    id: int
    group_id: int


class MemberUpdate(MemberCreate):
    stage_name: Optional[str] = None
    ex_member: Optional[bool] = None
    solo: Optional[bool] = None
    solo_debut: Optional[date] = None
    group_id: Optional[int] = None
    image_url: Optional[str] = None
    real_name: Optional[str] = None
    birthday: Optional[date] = None
    position: Optional[str] = None
