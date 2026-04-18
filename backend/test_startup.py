import asyncio
from main import app
from app.core.lifespan import lifespan

async def test_startup():
    print("Testing lifespan startup...")
    async with lifespan(app):
        print("Success: Lifespan started successfully.")
        print("db_pool:", getattr(app.state, "db_pool", None))
        print("semantic_router_available:", getattr(app.state, "semantic_router_available", False))
        
if __name__ == "__main__":
    asyncio.run(test_startup())
