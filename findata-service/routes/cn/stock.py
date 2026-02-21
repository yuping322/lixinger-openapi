"""中国市场股票接口"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional

from models import StandardResponse
from providers import LixingerProvider
from config import settings

router = APIRouter()

# 初始化 Provider
provider = LixingerProvider(settings.LIXINGER_TOKEN)


@router.get("/{symbol}/basic", response_model=StandardResponse)
async def get_stock_basic(symbol: str):
    """获取股票基础信息"""
    try:
        data = provider.get_stock_basic(symbol)

        if not data:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

        return StandardResponse(
            code=1,
            message="success",
            data=[data],
            meta={
                "source": "lixinger",
                "count": 1,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history", response_model=StandardResponse)
async def get_stock_history(
    symbol: str,
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="结束日期 YYYY-MM-DD"),
    period: str = Query("daily", description="周期: daily, weekly, monthly"),
    adjust: str = Query("ex_rights", description="复权类型: ex_rights, no_adjust")
):
    """获取股票历史行情"""
    try:
        data = provider.get_stock_history(symbol, start_date, end_date, period, adjust)

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


@router.get("/{symbol}/realtime", response_model=StandardResponse)
async def get_stock_realtime(symbol: str):
    """获取股票实时行情"""
    try:
        data = provider.get_stock_realtime(symbol)

        return StandardResponse(
            code=1,
            message="success",
            data=[data] if data else [],
            meta={
                "source": "lixinger",
                "count": 1 if data else 0,
                "timestamp": datetime.now().isoformat()
            },
            warnings=["理杏仁使用最新日线数据代替实时行情"] if data else ["无法获取实时行情数据"]
        )
    except Exception as e:
        # 不抛出异常，返回友好的错误信息
        return StandardResponse(
            code=1,
            message="success",
            data=[],
            meta={
                "source": "lixinger",
                "count": 0,
                "timestamp": datetime.now().isoformat()
            },
            warnings=["理杏仁免费版不提供实时行情，建议使用K线数据接口获取最新价格"],
            errors=[str(e)]
        )


@router.get("/{symbol}/financial", response_model=StandardResponse)
async def get_stock_financial(
    symbol: str,
    statement_type: str = Query(..., description="报表类型: balance_sheet, income_statement, cash_flow"),
    limit: int = Query(5, ge=1, le=20, description="返回记录数")
):
    """获取股票财务数据"""
    try:
        data = provider.get_financial_data(symbol, statement_type, limit)

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


@router.get("/{symbol}/valuation", response_model=StandardResponse)
async def get_stock_valuation(symbol: str):
    """获取股票估值指标"""
    try:
        data = provider.get_valuation(symbol)

        return StandardResponse(
            code=1,
            message="success",
            data=[data] if data else [],
            meta={
                "source": "lixinger",
                "count": 1 if data else 0,
                "timestamp": datetime.now().isoformat()
            },
            warnings=[] if data else ["理杏仁免费版可能不提供估值数据，或该股票暂无估值数据"]
        )
    except Exception as e:
        # 不抛出异常，返回友好的错误信息
        return StandardResponse(
            code=1,
            message="success",
            data=[],
            meta={
                "source": "lixinger",
                "count": 0,
                "timestamp": datetime.now().isoformat()
            },
            warnings=["理杏仁免费版不提供估值指标数据，建议升级订阅或使用其他数据源"],
            errors=[str(e)]
        )


@router.get("/{symbol}/profile", response_model=StandardResponse)
async def get_stock_profile(symbol: str):
    """获取公司概况"""
    try:
        # get_stock_basic returns company profile data when using profile endpoint
        from lixinger_openapi.query import query_json
        result = query_json("cn/company/profile", {"stockCodes": [symbol]})
        
        if result and result.get("code") == 1:
            data = result.get("data", [])
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
        else:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} profile not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/announcement", response_model=StandardResponse)
async def get_stock_announcement(
    symbol: str,
    limit: int = Query(10, ge=1, le=100, description="返回记录数")
):
    """获取公司公告"""
    try:
        data = provider.get_announcement(symbol, limit)
        
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
