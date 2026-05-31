from fastapi import APIRouter

from app.services.genius_service import GeniusService

router = APIRouter(prefix="/search", tags=["ПОИСК"])
service = GeniusService()

@router.get('', summary='ПОИСК')
async def search(q: str):
    results = service.search(q)
    return {
        'ok': True,
        'results': results
    }