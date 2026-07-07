import random

from app.services.song_model import Song
from app.utils.json_system import read_json, write_json

class PlaylistService:
    def __init__(self):
        self.playlist_path = "data/playlist.json"
        self.settings_path = "config/settings.json"
        self.playlist = []

    def create_playlist(self):
        settings = read_json(self.settings_path)
        playlist_json = read_json(self.playlist_path)['playlist']
        for i in playlist_json:
            name = playlist_json[i]["name"]
            authors = playlist_json[i]["artist"]
            priority = playlist_json[i]["priority"]
            img = playlist_json[i]["img"]
            self.playlist.append(Song(i, name, authors, priority, img, settings))
        multiplier = min(len(self.playlist), 200)
        for song in self.playlist:
            cd = settings.get(song.id)
            song.cooldown = int(cd * multiplier)
        return self.playlist

    def load_playlist(self):
        self.playlist = []
        data = read_json(self.playlist_path)
        playlist_json = data['playlist']
        stats_data = data.get('stats', {})
        settings = read_json(self.settings_path)
        for id in playlist_json:
            song = Song(
                id,
                playlist_json[id]["name"],
                playlist_json[id]["artist"],
                playlist_json[id]["priority"],
                playlist_json[id]["img"],
                settings
            )
            if id in stats_data:
                stat = stats_data[id]
                song.chance = stat.get("chance", song.chance)
                song.idle = stat.get("idle", song.idle)
                song.played = stat.get("played", song.played)
            self.playlist.append(song)
        multiplier = min(len(self.playlist), 200)
        for song in self.playlist:
            cd = settings[str(song.priority)]["cooldown"]
            song.cooldown = int(cd * multiplier)
        return self.playlist

    def save_playlist(self, img: str = None):
        data = read_json(self.playlist_path)
        playlist = data.get("playlist", {})
        stats = {}
        for song in self.playlist:
            song_id = str(song.id)
            stats[song_id] = {
                "chance": song.chance,
                "cooldown": song.cooldown,
                "up": song.up,
                "idle": song.idle,
                "played": song.played
            }
            if song_id not in playlist:
                playlist[song_id] = {
                    "name": song.name,
                    "artist": song.artist,
                    "img": img,
                    "priority": song.priority
                }
        data["playlist"] = playlist
        data["stats"] = stats
        write_json(self.playlist_path, data)

    def select_song(self):
        max_chance = max(song.chance for song in self.playlist)
        if max_chance >= 100:
            return max(self.playlist, key=lambda x: x.chance)
        r = random.randint(1, max(max_chance, 20))
        probably = []
        for song in self.playlist:
            if song.chance >= r:
                probably.append(song)
        if not (probably):
            return max(self.playlist, key=lambda x: x.chance)
        else:
            return random.choice(probably)

    def play_song(self):
        if not self.playlist:
            return None
        now_playing = self.select_song()
        for song in self.playlist:
            if song == now_playing: song.play()
            else: song.update()
        self.save_playlist()
        return now_playing

    def load_or_create(self):
        if not self.playlist:
            try:
                self.load_playlist()
            except:
                self.create_playlist()
                self.save_playlist()
        return self.playlist

    def get_playlist(self):
        playlist = {}
        for song in self.playlist:
            playlist[song.id] = song.to_dict()
        print(playlist)
        return playlist

    def delete_song(self, song_id: str):
        for song in self.playlist:
            if song.id == song_id:
                self.playlist.remove(song)
                self.save_playlist()
                return {
                    'ok': True,
                    'msg': f'Песня {song.name} удалена'
                }
        self.save_playlist()
        return {
            'ok': False,
            'err': f'Песня {song_id} не найдена в плейлисте'
        }

    def add_song(self, song_id: str, song_name: str, artist: list[str], priority: int, img: str):
        sett = read_json(self.settings_path)
        new_song = Song(song_id, song_name, artist, priority, img, sett)
        if new_song in self.playlist:
            return {
                'ok': False,
                'err': 'song is already in playlist'}
        self.playlist.append(new_song)
        self.save_playlist(img=img)
        return {
            'ok': True,
            'err': None
        }