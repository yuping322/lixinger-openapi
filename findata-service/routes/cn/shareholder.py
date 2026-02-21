"""股东信息接口"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/{symbol}", response_model=StandardResponse)
async def get_shareholders(symbol: str):
    """获取股东信息"""
    try:
        data = provider.get_shareholders(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["理杏仁免费版不提供股东详细信息，建议使用股东人数接口或其他数据源"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/count", response_model=StandardResponse)
async def get_shareholders_count(symbol: str):
    """获取股东人数"""
    try:
        data = provider.get_shareholders_count(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/executive", response_model=StandardResponse)
async def get_executive_shareholding(symbol: str):
    """获取高管增减持"""
    try:
        data = provider.get_executive_shareholding(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["理杏仁免费版不提供高管增减持数据，建议使用AKShare等替代数据源"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/major", response_model=StandardResponse)
async def get_major_shareholder_change(symbol: str):
    """获取大股东增减持"""
    try:
        data = provider.get_major_shareholder_change(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()},
            warnings=["理杏仁免费版不提供大股东增减持数据，建议使用AKShare等替代数据源"] if len(data) == 0 else []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/equity-change", response_model=StandardResponse)
async def get_equity_change(symbol: str):
    """获取股本变动数据"""
    try:
        data = provider.get_equity_change(symbol)
        return StandardResponse(
            code=1,
            message="success",
            data=data,
            meta={"source": "lixinger", "count": len(data), "timestamp": datetime.now().isoformat()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
