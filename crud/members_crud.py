from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import MemberModel, GroupModel
from schemas.member_schema import MemberCreate

def get_group_members(db: Session, group_id: int):
	statement = select(MemberModel).join(MemberModel.group).where(GroupModel.id == group_id)
	return db.scalars(statement).all()


def add_member(db: Session, group_id: int, new_member: MemberCreate):
	member = MemberModel(**new_member.model_dump())
	member.group_id = group_id
	db.add(member)
	db.commit()
	db.refresh(member)
	return member


def add_members(db: Session, group_id: int, new_members: List[MemberCreate]):
	for new_member in new_members:
		member = MemberModel(**new_member.model_dump())
		member.group_id = group_id
		db.add(member)
		db.commit()
		db.refresh(member)
	return get_group_members(db, group_id)


def get_member(db: Session, member_id: int):
	return db.query(MemberModel).filter_by(id=member_id).first()


def update_member(db: Session, member_id: int, new_memeber: dict):
	member = db.query(MemberModel).filter_by(id=member_id).first()

	if not member:
		return False
	
	for key, value in new_memeber.items():
		if hasattr(member, key):
			setattr(member, key, value)

	db.commit()
	db.refresh(member)

	return member


def delete_member(db: Session, member_id: int):
	member = db.query(MemberModel).filter_by(id = member_id).first()
	
	if member:
		db.delete(member)
		db.commit()
		return True
	
	return False