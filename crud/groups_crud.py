from sqlalchemy.orm import Session

from models import GroupModel, MemberModel
from schemas.group_schema import GroupCreate
from schemas.group_type import GroupType


def add_group(db: Session, schema: GroupCreate):
	group = GroupModel(**schema.model_dump())
	db.add(group)
	db.commit()
	db.refresh(group)
	return group


def get_groups(db: Session, skip: int = 0, limit: int = 10, type: GroupType = None):
	if type:
		return db.query(GroupModel).filter_by(type=type).offset(skip).limit(limit).all()
	return db.query(GroupModel).offset(skip).limit(limit).all()


def get_group(db: Session, group_id: int):
	group = db.query(GroupModel).filter_by(id=group_id).first()
	return group


def update_group(db: Session, group_id: int, new_group: dict):
	group = db.query(GroupModel).filter_by(id=group_id).first()

	if group is None:
		return False

	for key, value in new_group.items():
		if hasattr(group, key) and not value is None:
			setattr(group, key, value)

	db.commit()
	db.refresh(group)

	return group


def delete_group(db: Session, group_id: int):
	group = db.query(GroupModel).filter_by(id=group_id).first()
	if group is None:
		return "Group not found"
	members = db.query(MemberModel).filter_by(group_id=group_id).filter_by(solo = False).all()
	if members:
		return "Please delete non-solo members of the group first"

	db.delete(group)
	db.commit()

	return "Group deleted"

def delete_group_with_members(db: Session, group_id: int):
	group = db.query(GroupModel).filter_by(id=group_id).first()
	if group is None:
		return "Group not found"
	
	members = db.query(MemberModel).filter_by(group_id=group_id).filter_by(solo = False).all()
	if members:
		for member in members:
			db.delete(member)

	db.delete(group)
	db.commit()
	
	return "Group deleted with non-solo members"
