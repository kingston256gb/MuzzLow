from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, intpk
from app.models.playlist import PlaylistTable




class SongTable(Base):
    __tablename__ = 'songs'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
    youtube_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    genius_id: Mapped[int] = mapped_column(unique=True, nullable=False)

    artists: Mapped[list["ArtistTable"]] = relationship(
        secondary='song_artist',
        back_populates="songs",
    )
    playlists: Mapped[list["PlaylistTable"]] = relationship(
        secondary="playlist_songs",
        back_populates="songs"
    )



class ArtistTable(Base):
    __tablename__ = 'artists'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    genius_id: Mapped[int] = mapped_column(nullable=False, unique=True)

    songs: Mapped[list["SongTable"]] = relationship(
        secondary='song_artist',
        back_populates="artists"
    )


class SongArtistTable(Base):
    __tablename__ = 'song_artist'

    song_id: Mapped[int] = mapped_column(
        ForeignKey('songs.id', ondelete='CASCADE'),
        primary_key=True
    )
    artist_id: Mapped[int] = mapped_column(
        ForeignKey('artists.id', ondelete='CASCADE'),
        primary_key=True
    )