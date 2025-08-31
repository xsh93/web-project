from loguru import logger
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings, get_project_version, get_settings
from app.db.session import (
    setup_database_connection,
    close_database_connection,
    create_db_and_tables,
    get_db
)

# 使用lifespan管理应用生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()
    await setup_database_connection()
    if settings.ENVIRONMENT == "dev":
        await create_db_and_tables()

    logger.info("应用启动，数据库已连接。")
    yield
    # 应用关闭时执行
    await close_database_connection()
    logger.info("应用关闭，数据库连接已释放。")

app = FastAPI(
    title=settings.APP_NAME,
    description="Web project",
    version=get_project_version(),
    lifespan=lifespan,
)

@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(text("SELECT 1"))
        if results.scalar_one() == 1:
            return {"status": "ok", "message": "数据库连接成功！"}
    except Exception as e:
        return {"status": "error", "message": f"数据库连接失败：{e}"}


# if __name__ == "__main__":
#     main()
