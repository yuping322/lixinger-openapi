"""宏观经济接口"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()

# 初始化 Provider
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/lpr", response_model=StandardResponse)
async def get_lpr():
    """获取LPR利率"""
    try:
        data = provider.get_macro_data("lpr")

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


@router.get("/cpi", response_model=StandardResponse)
async def get_cpi():
    """获取CPI数据"""
    try:
        data = provider.get_macro_data("cpi")

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


@router.get("/ppi", response_model=StandardResponse)
async def get_ppi():
    """获取PPI数据"""
    try:
        data = provider.get_macro_data("ppi")

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


@router.get("/pmi", response_model=StandardResponse)
async def get_pmi():
    """获取PMI数据"""
    try:
        data = provider.get_macro_data("pmi")

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


@router.get("/m2", response_model=StandardResponse)
async def get_m2():
    """获取M2货币供应"""
    try:
        data = provider.get_macro_data("m2")

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
