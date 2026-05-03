import os


class Settings:
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL",
        "mongodb://health_user:health_password@localhost:27017/health_db?authSource=admin"
    )
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "health_db")


settings = Settings()
