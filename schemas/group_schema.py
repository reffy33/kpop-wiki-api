from pydantic import BaseModel
from typing import Optional
from datetime import date
from schemas.group_type import GroupType

# Group
class GroupCreate(BaseModel):
    name: str
    fandom_name: str
    agency: str
    type: GroupType
    image_url: Optional[str] = None
    hangul_name: Optional[str] = None
    debut_date: Optional[date] = None
    additional_info: Optional[str] = None


class GroupSchema(GroupCreate):
    id: int


class GroupUpdate(GroupCreate):
    name: Optional[str] = None
    fandom_name: Optional[str] = None
    agency: Optional[str] = None
    type: Optional[GroupType] = None
    image_url: Optional[str] = None
    hangul_name: Optional[str] = None
    debut_date: Optional[date] = None
    additional_info: Optional[str] = None