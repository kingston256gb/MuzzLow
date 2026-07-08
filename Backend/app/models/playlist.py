from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.models.base import Base, intpk
from app.models.song import SongTable


class PlaylistTable(Base):
    __tablename__ = 'playlists'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    position: Mapped[int] = mapped_column(nullable=True)

    songs: Mapped[list["SongTable"]] = relationship(
        secondary="playlist_songs",
        back_populates="playlists"
    )


class PlaylistSongTable(Base):
    __tablename__ = 'playlist_songs'

    song_id: Mapped[int] = mapped_column(
        ForeignKey('songs.id', ondelete='CASCADE'),
        primary_key=True,
        autoincrement=False
    )
    playlist_id: Mapped[int] = mapped_column(
        ForeignKey('playlists.id', ondelete='CASCADE'),
        primary_key=True,
        autoincrement=False
    )