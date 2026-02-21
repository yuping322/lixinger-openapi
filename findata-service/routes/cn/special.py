"""特殊数据接口"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/dragon-tiger/{symbol}", response_model=StandardResponse)
async def get_dragon_tiger(
    symbol: str,
    start_date: str = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(None, description="结束日期 YYYY-MM-DD")
):
    """获取龙虎榜数据"""
    try:
        data = provider.get_dragon_tiger(symbol, start_date, end_date)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["该股票在查询期间未上龙虎榜，或理杏仁免费版数据有限"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/block-deal/{symbol}", response_model=StandardResponse)
async def get_block_deal(symbol: str):
    """获取大宗交易数据"""
    try:
        data = provider.get_block_deal(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["理杏仁免费版不提供大宗交易数据，建议使用AKShare等替代数据源"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/equity-pledge/{symbol}", response_model=StandardResponse)
async def get_equity_pledge(symbol: str):
    """获取股权质押数据"""
    try:
        data = provider.get_equity_pledge(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["理杏仁免费版不提供股权质押数据，建议查询上交所/深交所官网或使用AKShare"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
