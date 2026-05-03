import os


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://auth_user:auth_password@localhost:3306/auth_db"
    )
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_key_e_sante_2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))
    JWT_REFRESH_EXPIRATION_DAYS: int = int(os.getenv("JWT_REFRESH_EXPIRATION_DAYS", "7"))
    HEALTH_SERVICE_URL: str = os.getenv("HEALTH_SERVICE_URL", "http://health-service:8000")


settings = Settings()
