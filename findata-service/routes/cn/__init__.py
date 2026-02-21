from fastapi import APIRouter
from .stock import router as stock_router
from .market import router as market_router
from .macro import router as macro_router
from .flow import router as flow_router
from .board import router as board_router
from .special import router as special_router
from .shareholder import router as shareholder_router
from .dividend import router as dividend_router

# 创建中国市场路由
router = APIRouter()

# 注册子路由
router.include_router(stock_router, prefix="/stock", tags=["Stock"])
router.include_router(market_router, prefix="/market", tags=["Market"])
router.include_router(macro_router, prefix="/macro", tags=["Macro"])
router.include_router(flow_router, prefix="/flow", tags=["Fund Flow"])
router.include_router(board_router, prefix="/board", tags=["Board"])
router.include_router(special_router, prefix="/special", tags=["Special Data"])
router.include_router(shareholder_router, prefix="/shareholder", tags=["Shareholder"])
router.include_router(dividend_router, prefix="/dividend", tags=["Dividend"])
