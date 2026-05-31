from fastapi import APIRouter

from app.models.song import Song
from app.services.playlist_service import PlaylistService

router = APIRouter(prefix="/playlist", tags=["ПЛЕЙЛИСТ"])
service = PlaylistService()

@router.get('/', summary='ПОЛУЧИТЬ ПЛЕЙЛИСТ')
async def get_playlist():
    service.load_or_create()
    return {
        "ok": True,
        "playlist": service.get_playlist()
    }

@router.post('/play', summary='СЫГРАТЬ ПЕСНЮ')
async def play_song():
    service.load_or_create()
    curr_song = service.play_song()
    return {
        "ok": True,
        "song": curr_song.to_dict(),
        "playlist": service.get_playlist()
    }

@router.delete('/{song_id}', summary='УДАЛИТЬ ПЕСНЮ')
async def delete_song(song_id: str):
    service.load_or_create()
    response = service.delete_song(song_id)
    if response['ok']:
        return {
            "ok": True,
            "msg": f'Песня {song_id} удалена',
            "playlist": service.get_playlist()
        }
    return {
        "ok": False,
        "err": response['err']
    }

@router.post('/add', summary='ДОБАВИТЬ ПЕСНЮ')
async def add_song(song_id: str, song_name: str, artist: list[str], priority: int, img: str = None):
    service.load_or_create()
    response = service.add_song(song_id, song_name, artist, priority, img)
    if response["ok"]:
        return {
            "ok": True,
            'msg': f'Пенся {song_name} добавлена в плейлист',
            "playlist": service.get_playlist()
        }
    else:
        return {
            "ok": False,
            "err": response["err"]
        }