"""行业板块接口"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/industry/list", response_model=StandardResponse)
async def get_industry_list():
    """获取行业列表"""
    try:
        data = provider.get_industry_list()
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industry/{industry_code}/kline", response_model=StandardResponse)
async def get_industry_kline(
    industry_code: str,
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="结束日期 YYYY-MM-DD")
):
    """获取行业K线数据"""
    try:
        data = provider.get_industry_kline(industry_code, start_date, end_date)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industry/{industry_code}/stocks", response_model=StandardResponse)
async def get_industry_stocks(industry_code: str):
    """获取行业成分股"""
    try:
        data = provider.get_industry_stocks(industry_code)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industry/{industry_code}/valuation", response_model=StandardResponse)
async def get_industry_valuation(industry_code: str):
    """获取行业估值数据"""
    try:
        data = provider.get_industry_valuation(industry_code)
        if not data:
            raise HTTPException(status_code=404, detail=f"Industry {industry_code} valuation not found")
        return StandardResponse(
            code=1,
            message="success",
            data=[data],
            meta={"source": "lixinger", "count": 1, "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/list", response_model=StandardResponse)
async def get_index_list():
    """获取指数列表"""
    try:
        data = provider.get_index_list()
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/{index_code}/kline", response_model=StandardResponse)
async def get_index_kline(
    index_code: str,
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="结束日期 YYYY-MM-DD")
):
    """获取指数K线数据"""
    try:
        data = provider.get_index_kline(index_code, start_date, end_date)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/index/{index_code}/constituents", response_model=StandardResponse)
async def get_index_constituents(index_code: str):
    """获取指数成分股"""
    try:
        data = provider.get_index_constituents(index_code)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
