from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field


class QueryType(str, Enum):
	CURRENT = "current"
	DAILY = "daily"
	HOURLY = "hourly"


class Unit(str, Enum):
	C = "c"
	F = "f"


class Lang(str, Enum):
	ZH_CN = "zh_cn"
	EN = "en"


class TianqiRequest(BaseModel):
	city: str = Field(..., description="城市名称/ID/经纬度字符串")
	date: Optional[str] = Field(None, description="ISO8601 或 today|tomorrow|+N")
	lang: Lang = Field(default=Lang.ZH_CN)
	unit: Unit = Field(default=Unit.C)
	type: QueryType = Field(default=QueryType.DAILY)


class Location(BaseModel):
	name: str
	id: Optional[str] = None
	lat: Optional[float] = None
	lon: Optional[float] = None
	timezone: Optional[str] = None


class CurrentWeather(BaseModel):
	temp: Optional[float] = None
	weather: Optional[str] = None
	humidity: Optional[float] = None
	windDir: Optional[str] = None
	windSpeed: Optional[float] = None


class DailyForecast(BaseModel):
	date: Optional[str] = None
	tempMax: Optional[float] = None
	tempMin: Optional[float] = None
	weatherDay: Optional[str] = None
	weatherNight: Optional[str] = None
	pop: Optional[float] = None


class HourlyForecast(BaseModel):
	time: Optional[str] = None
	temp: Optional[float] = None
	weather: Optional[str] = None
	pop: Optional[float] = None


class TianqiResponse(BaseModel):
	location: Location
	updateTime: Optional[str] = None
	unit: Unit
	current: Optional[CurrentWeather] = None
	forecast: Optional[List[DailyForecast]] = None
	hourly: Optional[List[HourlyForecast]] = None
	raw: Optional[Any] = None  # 供应商原始响应（便于排查）


class ErrorModel(BaseModel):
	code: str
	message: str
	details: Optional[Any] = None
