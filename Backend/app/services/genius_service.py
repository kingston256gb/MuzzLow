import re
from lyricsgenius import Genius
from dotenv import load_dotenv
from os import getenv

load_dotenv(dotenv_path=".env")
TOKEN = getenv("GENIUS_TOKEN")

class GeniusService:
    def __init__(self):
        self.genius = Genius(TOKEN)
        self.genius.verbose = False

    def clean(self, name:str):
        has_cyrillic = any('\u0400' <= c <= '\u04FF' for c in name)
        if has_cyrillic:
            cleaned = re.sub(r'\s*\([^()]*[A-Za-z][^()]*\)$', '', name)
            cleaned = re.sub(r'\s*\([A-Za-z\s!&]+\)', '', cleaned)
            return cleaned.strip() if cleaned.strip() else name
        return name

    def search(self, prompt: str):
        search_results = self.genius.search_all(prompt, per_page=5)
        results = []
        for section in search_results["sections"]:
            for result in section["hits"]:
                if result["index"] == "lyric":
                    continue
                elif result["index"] == "article":
                    continue
                elif result["index"] == "song":
                    data = result["result"]
                    song_name = self.clean(data["title"])
                    song_id = str(data["id"])
                    img = data["header_image_thumbnail_url"]
                    song_artists_data = data["primary_artists"]
                    artists = []
                    for artist in song_artists_data:
                        artist_name = self.clean(artist["name"])
                        if 'Genius' in artist_name:
                            continue
                        else:
                            artists.append(artist_name)
                    if artists:
                        res = {
                            "name": song_name,
                            "artist": artists,
                            "id": song_id,
                            "img": img
                        }
                        if res not in results: results.append(res)
                elif result["index"] == "artist":
                    data = result["result"]
                    artist_name = self.clean(data["name"])
                    artist_id = data["id"]
                    if artist_name.lower() == prompt.lower() or artist_name.lower().startswith(prompt.lower()):
                        songs = self.genius.search_artist_songs(artist_id, artist_name, per_page=10, sort='popularity')
                        for song in songs["songs"]:
                            song_name = self.clean(song["title"])
                            song_artists_data = song["primary_artists"]
                            img = song["header_image_thumbnail_url"]
                            artists = []
                            song_id = str(song["id"])
                            for artist in song_artists_data:
                                artist_name = self.clean(artist["name"])
                                artists.append(artist_name)
                            res = {
                                "name": song_name,
                                "artist": artists,
                                "id": song_id,
                                "img": img
                            }
                            if res not in results: results.append(res)
        return results