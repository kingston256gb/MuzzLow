from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.models.base import Base, intpk

class UserQueueTable(Base):
    __tablename__ = 'user_queue'

    song_id: Mapped[int] = mapped_column(
        ForeignKey('songs.id', ondelete='CASCADE')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
        autoincrement=False
    )
    position: Mapped[intpk] = mapped_column(autoincrement=False)