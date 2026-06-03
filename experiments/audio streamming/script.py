import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_URL = 'https://inv.thepixora.com/api/v1'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

@app.get('/music')
async def find_music(q: str):
    search_response = requests.get(
        f'{BASE_URL}/search',
        params={'q': q},
        headers=headers
    )
    search_response.raise_for_status()
    search_data = search_response.json()
    if not search_data:
        return {'error': 'Nothing found'}
    video_id = search_data[0]['videoId']
    video_response = requests.get(
        f'{BASE_URL}/videos/{video_id}',
        headers=headers
    )
    video_response.raise_for_status()
    video_data = video_response.json()
    audio_formats = [
        f for f in video_data["adaptiveFormats"]
        if f["type"].startswith("audio/")
    ]
    best_audio = max(
        audio_formats,
        key=lambda x: int(x.get("bitrate", 0))
    )

    return {
        "videoId": video_id,
        "audioUrl": best_audio["url"],
    }

@app.get("/test")
async def test(a: str):
    r = requests.get(a, stream=True)
    print(r.status_code)

    return {
        "status": r.status_code,
        "content_type": r.headers.get("content-type")
    }


@app.get('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    uvicorn.run('script:app', reload=True)