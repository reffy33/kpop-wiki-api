from typing import List, Optional
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date
from schemas.group_type import GroupType


class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class GroupModel(Base):
	__tablename__ = "groups"

	name: Mapped[str] = mapped_column(String(100))
	image_url: Mapped[Optional[str]]
	fandom_name: Mapped[str] = mapped_column(String(100))
	type: Mapped[Enum] = mapped_column(Enum(GroupType))
	hangul_name: Mapped[Optional[str]] = mapped_column(String(100))
	debut_date: Mapped[Optional[date]]
	agency: Mapped[str] = mapped_column(String(100))
	additional_info: Mapped[Optional[str]]
	members: Mapped[Optional[List["MemberModel"]]] = relationship(back_populates="group", uselist=False)

	def __repr__(self) -> str:
		return f"Group(id={self.id}, name={self.name}, fandom_name={self.fandom_name}, agency={self.agency}, type={self.type})"


class MemberModel(Base):
	__tablename__ = "members"

	stage_name: Mapped[str] = mapped_column(String(100))
	image_url: Mapped[Optional[str]]
	real_name: Mapped[Optional[str]] = mapped_column(String(100))
	birthday: Mapped[Optional[date]]
	position: Mapped[Optional[str]]
	ex_member: Mapped[bool] = mapped_column(default=False)
	solo: Mapped[bool] = mapped_column(default=False)
	solo_debut: Mapped[Optional[date]]
	group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"))
	group: Mapped[Optional["GroupModel"]] = relationship(back_populates="members", uselist=False)

	def __repr__(self) -> str:
		return f"Member(id={self.id}, stage_name={self.stage_name}, group={self.group_id})"


if __name__ == '__main__':
	from database import engine
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)