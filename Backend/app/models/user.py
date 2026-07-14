from datetime import datetime, timezone
from time import timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from enum import Enum

from app.models.base import Base, intpk


class UserTable(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)

    bans: Mapped[list["BannedUserTable"]] = relationship(
        back_populates="user",
        lazy="selectin",
        primaryjoin="and_(UserTable.id == BannedUserTable.user_id, BannedUserTable.is_active == True)"
    )


class UserStatsTable(Base):
    __tablename__ = 'user_stats'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
        autoincrement=False
    )
    song_id: Mapped[int] = mapped_column(
        ForeignKey('songs.id', ondelete='CASCADE'),
        primary_key=True,
        autoincrement=False
    )

    priority: Mapped[int]
    played: Mapped[int]
    idle: Mapped[int]
    cooldown: Mapped[int]
    up: Mapped[int]



class BanCode(str, Enum):
    JL = "JL"
    JS = "JS"
    AS = "AS"
    MB = "MB"
    HD = "HD"

    @property
    def desc(self) -> str:
        descs = {
            BanCode.JL: "Your JWT or cookies were stolen or you sent them to another user",
            BanCode.JS: "This JWT is owned by another user",
            BanCode.AS: "API spam detected",
            BanCode.MB: "Banned by Administrator",
            BanCode.HD: "Hacker detected. SQL injection or malicious payload attempt"
        }
        return descs.get(self)



class BannedUserTable(Base):
    __tablename__ = 'banned_users'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    ban_code: Mapped[BanCode] = mapped_column(nullable=False)
    banned_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    ban_duration: Mapped[int | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["UserTable"] = relationship(back_populates="bans")