from fastapi import HTTPException
from prisma import Prisma
from prisma.errors import PrismaError


async def get_db_connection():
    db = Prisma()
    try:
        await db.connect()
        yield db
    except PrismaError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prisma error: Database connection failed. Error: {str(e)}",
        )
    finally:
        if db.is_connected():
            await db.disconnect()