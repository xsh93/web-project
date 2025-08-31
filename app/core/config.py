import os
from functools import lru_cache
from typing import Literal
from importlib import metadata

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- 动态版本号获取 ---
def get_project_version() -> str:
    """从 pyproject.toml 文件中动态读取项目版本号。"""
    try:
        return metadata.version("web-project")
    except metadata.PackageNotFoundError:
        return "0.1.0-dev"

# --- 嵌套配置模型 ---
class DatabaseSettings(BaseSettings):
    """数据库相关配置"""
    HOST: str = "localhost"
    PORT: int = 5432
    USERNAME: str = "admin"
    PASSWORD: str = "123456"
    DB: str = "app"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """异步PostgreSQL"""
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    model_config = SettingsConfigDict(env_prefix="DEMO_DB_")

class Settings(BaseSettings):
    """主配置类，汇集所有配置项。"""
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    DEBUG: bool = False
    APP_NAME: str = "web-project"

    # --- 嵌套配置模型 ---
    DB: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_prefix="DEMO_",
        case_sensitive=False,
    )

# --- 缓存与依赖注入 ---
@lru_cache
def get_settings() -> Settings:
    """创建并返回一个配置实例"""

    print("正在加载配置...")

    env = os.getenv("ENVIRONMENT", "dev")
    env_file = f".env.{env}"
    settings = Settings(_env_file=env_file)
    print(f"成功加载 '{env}' 环境配置 for {settings.APP_NAME}")
    return settings

settings = get_settings()