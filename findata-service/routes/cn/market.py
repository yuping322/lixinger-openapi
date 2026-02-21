"""中国市场接口"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()

# 初始化 Provider
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/overview", response_model=StandardResponse)
async def get_market_overview():
    """获取市场概览"""
    try:
        data = provider.get_market_overview()

        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={
                "source": "lixinger",
                "count": len(data),
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
