from __future__ import annotations

from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class AuthMode(str, Enum):
	HEADER_APPCODE = "header_appcode"
	QUERY_KEY_SECRET = "query_key_secret"


class Settings(BaseSettings):
	# Auth
	YIYUAN_AUTH_MODE: AuthMode = Field(default=AuthMode.HEADER_APPCODE)
	YIYUAN_APPCODE: str | None = None
	YIYUAN_APPKEY: str | None = None
	YIYUAN_APPSECRET: str | None = None

	# Endpoints
	YIYUAN_BASE_URL: str = Field(default="")
	YIYUAN_WEATHER_PATH_CURRENT: str | None = None
	YIYUAN_WEATHER_PATH_DAILY: str | None = None
	YIYUAN_WEATHER_PATH_HOURLY: str | None = None

	# Runtime
	LOG_LEVEL: str = Field(default="INFO")
	HTTP_TIMEOUT_SECONDS: int = Field(default=10)
	HTTP_MAX_RETRIES: int = Field(default=2)
	CACHE_TTL_SECONDS: int = Field(default=300)
	ENABLE_CACHE: bool = Field(default=True)

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	return Settings()  # type: ignore[call-arg]
