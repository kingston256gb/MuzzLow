from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models.base import Base, intpk


class UserTable(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(nullable=False)


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