import sys
import asyncio
import logging

if sys.platform == "win32":
    # CRITICAL FIX for Windows:
    # psycopg async driver crashes on Windows if ProactorEventLoop is used.
    # Set the policy before Uvicorn or asyncio does anything.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logging.info("Set WindowsSelectorEventLoopPolicy for async database compatibility.")

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.APP_DEBUG)
