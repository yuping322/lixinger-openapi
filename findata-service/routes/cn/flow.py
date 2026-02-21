"""资金流向接口"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/stock/{symbol}", response_model=StandardResponse)
async def get_stock_fund_flow(symbol: str):
    """获取个股资金流向"""
    try:
        data = provider.get_fund_flow_stock(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/{index_code}", response_model=StandardResponse)
async def get_index_fund_flow(index_code: str):
    """获取指数资金流向"""
    try:
        data = provider.get_fund_flow_index(index_code)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industry", response_model=StandardResponse)
async def get_industry_fund_flow(industry_code: str = Query(None, description="行业代码，不填则返回所有行业")):
    """获取行业资金流向"""
    try:
        data = provider.get_fund_flow_industry(industry_code)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
