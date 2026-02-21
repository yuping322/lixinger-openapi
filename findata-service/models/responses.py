"""数据模型"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseMeta(BaseModel):
    """响应元数据"""
    source: str = "lixinger"
    cached: bool = False
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    count: int = 0


class StandardResponse(BaseModel):
    """标准响应格式"""
    code: int = 1
    message: str = "success"
    data: List[Dict[str, Any]] = []
    meta: ResponseMeta = ResponseMeta()
    warnings: List[str] = []
    errors: List[str] = []


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int = 0
    message: str
    errors: List[str]
