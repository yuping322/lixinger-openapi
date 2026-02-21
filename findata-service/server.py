#!/usr/bin/env python3
"""Findata Service 主服务"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

from routes.cn import router as cn_router
from config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="Findata Service",
    description="统一金融数据服务 API - 基于理杏仁数据源",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(cn_router, prefix="/api/cn", tags=["China Market"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "Findata Service",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # 验证配置
    try:
        settings.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请检查 .env 文件并设置 LIXINGER_TOKEN")
        exit(1)

    # 启动服务
    print(f"Starting Findata Service on {settings.SERVICE_HOST}:{settings.SERVICE_PORT}")
    print(f"API 文档: http://localhost:{settings.SERVICE_PORT}/docs")

    uvicorn.run(
        app,
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
