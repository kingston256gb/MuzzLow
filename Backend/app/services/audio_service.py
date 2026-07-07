import yt_dlp


class AudioService:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True
        }
        self.query_base = "ytsearch1:"

    def get_audio_link(self, q: str):
        """ Get link to play audio with using YouTube search (atrist, songName) """
        query = self.query_base + q
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                data = info['entries'][0]['formats']
                audio_formats = [item for item in data
                                 if item.get('vcodec') == 'none'
                                 and item.get('acodec') != 'none']

                best_audio_url = max(audio_formats, key=lambda x: x.get('abr', 0))['url']

                if best_audio_url:
                    return best_audio_url
                return

            except:
                return