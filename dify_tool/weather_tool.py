#!/usr/bin/env python3
"""
Dify天气工具实现
提供天气查询功能给Dify平台使用
"""

import requests
import json
from typing import Dict, Any, Optional

class WeatherTool:
    """天气查询工具类"""
    
    def __init__(self, api_base_url: str = "https://weather-api-slct.onrender.com"):
        """
        初始化天气工具
        
        Args:
            api_base_url: API服务的基础URL
        """
        self.api_base_url = api_base_url.rstrip('/')
    
    def get_current_weather(self, city: str) -> Dict[str, Any]:
        """
        获取指定城市的当前天气
        
        Args:
            city: 城市名称
            
        Returns:
            包含天气信息的字典
        """
        try:
            url = f"{self.api_base_url}/weather"
            params = {"city": city}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 格式化返回数据，使其更适合Dify使用
            return {
                "success": True,
                "data": {
                    "city": data.get("city", city),
                    "temperature": data.get("temperature"),
                    "description": data.get("description"),
                    "humidity": data.get("humidity")
                },
                "message": f"{data.get('city', city)}的当前天气：{data.get('description')}，温度{data.get('temperature')}°C，湿度{data.get('humidity')}%"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}",
                "message": f"无法获取{city}的天气信息，请检查网络连接或稍后重试"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取天气信息失败: {str(e)}",
                "message": f"获取{city}天气信息时发生错误"
            }
    
    def format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """
        格式化天气响应为可读文本
        
        Args:
            weather_data: 天气数据字典
            
        Returns:
            格式化的天气信息文本
        """
        if not weather_data.get("success", False):
            return weather_data.get("message", "获取天气信息失败")
        
        data = weather_data.get("data", {})
        city = data.get("city", "未知城市")
        temperature = data.get("temperature", "未知")
        description = data.get("description", "未知")
        humidity = data.get("humidity", "未知")
        
        return f"""🌤️ {city}天气信息：
📍 城市：{city}
🌡️ 温度：{temperature}°C
☁️ 天气：{description}
💧 湿度：{humidity}%"""
    
    def invoke(self, city: str) -> str:
        """
        Dify工具调用接口
        
        Args:
            city: 城市名称
            
        Returns:
            格式化的天气信息
        """
        weather_data = self.get_current_weather(city)
        return self.format_weather_response(weather_data)

# 工具实例
weather_tool = WeatherTool()

def get_weather(city: str) -> str:
    """
    Dify工具函数 - 获取天气信息
    
    Args:
        city: 城市名称
        
    Returns:
        天气信息文本
    """
    return weather_tool.invoke(city)

# 测试函数
if __name__ == "__main__":
    # 测试工具功能
    test_cities = ["北京", "上海", "广州", "深圳"]
    
    for city in test_cities:
        print(f"\n测试城市: {city}")
        result = get_weather(city)
        print(result)
