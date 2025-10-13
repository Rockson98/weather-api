#!/usr/bin/env python3
"""
OpenWeatherMap API客户端
支持当前天气、天气预报、地理编码等功能
"""

import asyncio
import aiohttp
import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WeatherData:
    """天气数据结构"""
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    wind_direction: int
    visibility: int
    uv_index: Optional[float] = None
    timestamp: Optional[str] = None

@dataclass
class ForecastData:
    """天气预报数据结构"""
    city: str
    country: str
    forecast: List[Dict[str, Any]]

class OpenWeatherClient:
    """OpenWeatherMap API客户端"""
    
    def __init__(self):
        # 直接使用我们的API密钥
        self.api_key = "811a271ed44e1d5599d8e0c773417557"
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        self.timeout = 10
        self.max_retries = 2
        
        # 调试信息
        logger.info(f"Using API key: {self.api_key[:8]}...")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送HTTP请求"""
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    response_text = await response.text()
                    raise Exception(f"Invalid API key. Status: {response.status}, Response: {response_text}")
                elif response.status == 404:
                    response_text = await response.text()
                    raise Exception(f"City not found. Status: {response.status}, Response: {response_text}")
                elif response.status == 429:
                    raise Exception("API rate limit exceeded")
                else:
                    response_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}, Response: {response_text}")
    
    async def get_current_weather(self, city: str, country_code: str = None) -> WeatherData:
        """获取当前天气"""
        try:
            # 构建查询参数
            query = f"{city},{country_code}" if country_code else city
            
            url = f"{self.base_url}/weather"
            params = {
                'q': query,
                'appid': self.api_key,
                'units': 'metric',  # 使用摄氏度
                'lang': 'zh_cn'      # 中文描述
            }
            
            logger.info(f"Fetching current weather for {city}")
            data = await self._make_request(url, params)
            
            # 解析响应数据
            weather_data = WeatherData(
                city=data['name'],
                country=data['sys']['country'],
                temperature=data['main']['temp'],
                feels_like=data['main']['feels_like'],
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                description=data['weather'][0]['description'],
                icon=data['weather'][0]['icon'],
                wind_speed=data['wind']['speed'],
                wind_direction=data['wind'].get('deg', 0),
                visibility=data.get('visibility', 0) / 1000,  # 转换为公里
                timestamp=data['dt']
            )
            
            logger.info(f"Successfully fetched weather for {city}")
            return weather_data
            
        except Exception as e:
            logger.error(f"Error fetching current weather for {city}: {e}")
            raise
    
    async def get_forecast(self, city: str, country_code: str = None, days: int = 5) -> ForecastData:
        """获取天气预报"""
        try:
            query = f"{city},{country_code}" if country_code else city
            
            url = f"{self.base_url}/forecast"
            params = {
                'q': query,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'zh_cn',
                'cnt': days * 8  # 每天8个数据点（每3小时一个）
            }
            
            logger.info(f"Fetching forecast for {city}")
            data = await self._make_request(url, params)
            
            # 解析预报数据
            forecast_list = []
            for item in data['list']:
                forecast_item = {
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind'].get('deg', 0),
                    'precipitation': item.get('rain', {}).get('3h', 0)
                }
                forecast_list.append(forecast_item)
            
            forecast_data = ForecastData(
                city=data['city']['name'],
                country=data['city']['country'],
                forecast=forecast_list
            )
            
            logger.info(f"Successfully fetched forecast for {city}")
            return forecast_data
            
        except Exception as e:
            logger.error(f"Error fetching forecast for {city}: {e}")
            raise
    
    async def search_city(self, city_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """搜索城市"""
        try:
            url = f"{self.base_url}/find"
            params = {
                'q': city_name,
                'appid': self.api_key,
                'limit': limit
            }
            
            logger.info(f"Searching for city: {city_name}")
            data = await self._make_request(url, params)
            
            cities = []
            for item in data['list']:
                city_info = {
                    'name': item['name'],
                    'country': item['sys']['country'],
                    'lat': item['coord']['lat'],
                    'lon': item['coord']['lon']
                }
                cities.append(city_info)
            
            logger.info(f"Found {len(cities)} cities for {city_name}")
            return cities
            
        except Exception as e:
            logger.error(f"Error searching for city {city_name}: {e}")
            raise

# 测试函数
async def test_openweather_api():
    """测试OpenWeatherMap API"""
    try:
        client = OpenWeatherClient()
        
        # 测试当前天气
        print("测试当前天气...")
        weather = await client.get_current_weather("Beijing")
        print(f"城市: {weather.city}, {weather.country}")
        print(f"温度: {weather.temperature}°C")
        print(f"体感温度: {weather.feels_like}°C")
        print(f"湿度: {weather.humidity}%")
        print(f"气压: {weather.pressure} hPa")
        print(f"描述: {weather.description}")
        print(f"风速: {weather.wind_speed} m/s")
        
        # 测试天气预报
        print("\n测试天气预报...")
        forecast = await client.get_forecast("Beijing", days=3)
        print(f"城市: {forecast.city}, {forecast.country}")
        print(f"预报天数: {len(forecast.forecast)}")
        
        print("OpenWeatherMap API测试成功！")
        
    except Exception as e:
        print(f"API测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_openweather_api())
