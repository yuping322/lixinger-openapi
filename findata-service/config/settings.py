"""配置管理"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings:
    """配置类"""

    # 理杏仁配置
    LIXINGER_TOKEN: str = os.getenv("LIXINGER_TOKEN", "")

    # 服务配置
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "0.0.0.0")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8000"))

    # 缓存配置
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"

    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        """验证配置"""
        if not self.LIXINGER_TOKEN:
            raise ValueError("LIXINGER_TOKEN is required. Please set it in .env file")


settings = Settings()
