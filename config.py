"""Configuration settings for the AVM MCP Server."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Server configuration
    MCP_HOST: str = "0.0.0.0"
    MCP_PORT: int = 8080
    MCP_DEBUG: bool = False
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()


# Logging configuration
# Note: Uses stderr to avoid interfering with MCP STDIO transport
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "level": settings.LOG_LEVEL,
        "handlers": ["console"],
    },
}
