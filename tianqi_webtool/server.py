from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas import (
	TianqiRequest,
	TianqiResponse,
	ErrorModel,
	Location,
	CurrentWeather,
	DailyForecast,
	HourlyForecast,
	QueryType,
	Unit,
)
from .openweather_client import OpenWeatherClient

app = FastAPI(title="TianqiWebTool")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "TianqiWebTool API", "status": "running"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy", "service": "TianqiWebTool"}


def _parse_percent_to_float(value: Optional[str]) -> Optional[float]:
	if value is None:
		return None
	try:
		return float(value.replace("%", ""))
	except Exception:
		return None


def _yyyymmdd_to_date(value: Optional[str]) -> Optional[str]:
	if not value:
		return None
	if len(value) == 8:
		return f"{value[0:4]}-{value[4:6]}-{value[6:8]}"
	return value


def _time_to_iso8601(raw_time: Optional[str], tz_offset: Optional[str]) -> Optional[str]:
	# raw_time: yyyymmddHHMMSS, tz_offset: "+8" like
	if not raw_time:
		return None
	try:
		dt = datetime.strptime(raw_time, "%Y%m%d%H%M%S")
		# 不强行加时区，保留本地/未知；如需可拼接 tz_offset
		return dt.isoformat()
	except Exception:
		return None


def map_openweather_response(weather_data, req: TianqiRequest) -> TianqiResponse:
	"""映射OpenWeatherMap响应到标准格式"""
	from datetime import datetime
	
	location = Location(
		name=weather_data.city,
		id=None,
		lat=None,
		lon=None,
		timezone=None,
	)
	unit = Unit.C
	update_time = datetime.fromtimestamp(weather_data.timestamp).isoformat() if weather_data.timestamp else None

	if req.type == QueryType.CURRENT:
		current = CurrentWeather(
			temp=weather_data.temperature,
			weather=weather_data.description,
			humidity=weather_data.humidity,
			windDir=f"{weather_data.wind_direction}°",
			windSpeed=weather_data.wind_speed,
		)
		return TianqiResponse(location=location, updateTime=update_time, unit=unit, current=current, raw=weather_data.__dict__)

	# 对于预报，返回空列表（需要实现预报功能）
	forecast: List[DailyForecast] = []
	hourly: List[HourlyForecast] = []
	return TianqiResponse(location=location, updateTime=update_time, unit=unit, forecast=forecast, hourly=hourly, raw=weather_data.__dict__)


@app.post("/tool/tianqi/query")
async def tool_tianqi_query(req: TianqiRequest):
	client = OpenWeatherClient()
	try:
		if req.type.value == "current":
			weather_data = await client.get_current_weather(req.city)
			data = map_openweather_response(weather_data, req)
		elif req.type.value == "daily":
			# 暂时返回当前天气，后续可以实现预报功能
			weather_data = await client.get_current_weather(req.city)
			data = map_openweather_response(weather_data, req)
		else:
			# 暂时返回当前天气，后续可以实现小时预报功能
			weather_data = await client.get_current_weather(req.city)
			data = map_openweather_response(weather_data, req)
		return JSONResponse(content=data.model_dump())
	except Exception as e:
		err = ErrorModel(code="PROVIDER_ERROR", message=str(e))
		return JSONResponse(status_code=500, content=err.model_dump())
