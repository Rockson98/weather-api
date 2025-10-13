from __future__ import annotations

from typing import Any, Dict, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import get_settings, AuthMode


class YiYuanClient:
	def __init__(self) -> None:
		self.settings = get_settings()
		self.client = httpx.AsyncClient(timeout=self.settings.HTTP_TIMEOUT_SECONDS)

	def _build_url(self, path: Optional[str]) -> str:
		base = (self.settings.YIYUAN_BASE_URL or "").rstrip("/")
		if not base:
			raise ValueError("YIYUAN_BASE_URL 未配置")
		if not path:
			return base
		if path.startswith("http"):
			return path
		return f"{base}/{path.lstrip('/')}"

	def _auth_headers(self) -> Dict[str, str]:
		if self.settings.YIYUAN_AUTH_MODE == AuthMode.HEADER_APPCODE:
			if not self.settings.YIYUAN_APPCODE:
				raise ValueError("YIYUAN_APPCODE 未配置")
			return {"Authorization": f"APPCODE {self.settings.YIYUAN_APPCODE}"}
		return {}

	@retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=3), stop=stop_after_attempt(1))
	async def _get(self, url: str, params: Dict[str, Any]) -> httpx.Response:
		headers = self._auth_headers()
		resp = await self.client.get(url, headers=headers, params=params)
		resp.raise_for_status()
		return resp

	async def query_current(self, city: str) -> Dict[str, Any]:
		url = self._build_url(self.settings.YIYUAN_WEATHER_PATH_CURRENT)
		# 实况：needMoreDay=0&need3HourForcast=0
		resp = await self._get(url, {"area": city, "needMoreDay": 0, "need3HourForcast": 0})
		return resp.json()

	async def query_daily(self, city: str) -> Dict[str, Any]:
		url = self._build_url(self.settings.YIYUAN_WEATHER_PATH_DAILY)
		# 多日：needMoreDay=1
		resp = await self._get(url, {"area": city, "needMoreDay": 1, "need3HourForcast": 0})
		return resp.json()

	async def query_hourly(self, city: str) -> Dict[str, Any]:
		url = self._build_url(self.settings.YIYUAN_WEATHER_PATH_HOURLY)
		# 三小时：need3HourForcast=1（映射待样例完善）
		resp = await self._get(url, {"area": city, "needMoreDay": 0, "need3HourForcast": 1})
		return resp.json()

	async def aclose(self) -> None:
		await self.client.aclose()
