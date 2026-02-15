"""
金融数据工具包配置管理器
加载数据源配置和API密钥。
"""
import os
import json
import sys
from pathlib import Path


# 基础路径
SCRIPT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"
LIXINGER_ROOT = PROJECT_DIR.parent.parent / "lixinger-data-query"


def get_lixinger_token() -> str:
    """从 token.cfg 或环境变量获取理杏仁 Token。"""
    # 1. 检查环境变量
    token = os.getenv("LIXINGER_TOKEN")
    if token:
        return token
    
    # 2. 检查项目根目录下的 token.cfg
    token_cfg_path = PROJECT_DIR.parent.parent.parent / "token.cfg"
    if token_cfg_path.exists():
        try:
            with open(token_cfg_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    # 如果包含 [ 则尝试作为 configparser 解析
                    if content.startswith("["):
                        import configparser
                        config = configparser.ConfigParser()
                        config.read_string(content)
                        return config.get("lixinger", "token", fallback="")
                    else:
                        return content
        except Exception:
            pass
    return ""


def get_metadata_path() -> Path:
    """获取理杏仁元数据定义文件的路径。"""
    # 优先使用本地副本（如果存在）
    local_meta = PROJECT_DIR / "resources" / "metadata.json"
    if local_meta.exists():
        return local_meta
    
    # 否则尝试查找同级技能库中的原始文件
    remote_meta = LIXINGER_ROOT / "resources" / "metadata.json"
    return remote_meta


def get_config() -> dict:
    """从 YAML 加载配置或返回默认值。"""
    try:
        import yaml
        config_path = CONFIG_DIR / "data_sources.yaml"
        if config_path.exists():
            with open(config_path) as f:
                cfg = yaml.safe_load(f)
            _resolve_env_vars(cfg)
            return cfg
    except ImportError:
        pass

    # 回退默认值
    return {
        "china_market": {
            "primary": {
                "stock_data": "lixinger",
            },
        },
        "rate_limits": {
            "lixinger": 5,
        },
    }


def _resolve_env_vars(obj):
    """递归解析配置值中的 ${ENV_VAR} 引用。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[k] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[i] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
