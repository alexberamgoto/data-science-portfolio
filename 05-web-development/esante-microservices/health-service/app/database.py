from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    """Initialize the MongoDB async connection."""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DATABASE]
    # Test connection
    await client.admin.command("ping")
    print("✅ Health Service: Connected to MongoDB")


async def close_mongodb_connection():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        print("🛑 Health Service: MongoDB connection closed")


def get_database():
    """Return the database instance."""
    return db
