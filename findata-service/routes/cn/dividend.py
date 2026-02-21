"""分红配股接口"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/{symbol}", response_model=StandardResponse)
async def get_dividend(symbol: str):
    """获取分红送配数据"""
    try:
        data = provider.get_dividend(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
