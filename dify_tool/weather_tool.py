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
            
            # 直接返回API数据，确保格式与Dify代码执行节点期望一致
            return {
                "city": data.get("city", city),
                "temperature": data.get("temperature"),
                "description": data.get("description"),
                "humidity": data.get("humidity")
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "city": city,
                "temperature": 0,
                "description": "网络请求失败",
                "humidity": 0,
                "error": f"网络请求失败: {str(e)}"
            }
        except Exception as e:
            return {
                "city": city,
                "temperature": 0,
                "description": "获取天气信息失败",
                "humidity": 0,
                "error": f"获取天气信息失败: {str(e)}"
            }
    
    def format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """
        格式化天气响应为可读文本
        
        Args:
            weather_data: 天气数据字典
            
        Returns:
            格式化的天气信息文本
        """
        # 检查是否有错误
        if "error" in weather_data:
            return f"❌ 获取天气信息失败: {weather_data.get('error', '未知错误')}"
        
        city = weather_data.get("city", "未知城市")
        temperature = weather_data.get("temperature", "未知")
        description = weather_data.get("description", "未知")
        humidity = weather_data.get("humidity", "未知")
        
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
