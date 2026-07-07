from fastapi import APIRouter

from app.services.song_model import Song
from app.services.playlist_service import PlaylistService
from app.services.audio_service import AudioService

router = APIRouter(prefix="/playlist", tags=["ПЛЕЙЛИСТ"])
service = PlaylistService()
audio = AudioService()

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
    artist_str = ', '.join(curr_song.artist)
    url = audio.get_audio_url(f'{curr_song.name} {artist_str}')
    if url:
        return {
            "ok": True,
            "meta": curr_song.to_dict(),
            "url": url
        }
    else:
        return {
            "ok": False,
            "msg": 'Не удалось получить ссылку для проигрывания'
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
        "msg": response['err']
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
            "msg": response["err"]
        }