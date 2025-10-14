#!/usr/bin/env python3
"""
Dify代码执行节点 - 最小化解决方案
只返回工作流中实际需要的字段，避免验证错误
"""

def main(arg1, arg2):
    """
    arg1: 天气API返回的数据
    arg2: 城市名称
    """
    
    # 处理天气数据
    weather_data = arg1
    if isinstance(weather_data, list) and len(weather_data) > 0:
        weather_data = weather_data[0]
    if not isinstance(weather_data, dict):
        weather_data = {}
    
    # 提取天气信息，确保所有字段都有值
    city = weather_data.get('city', arg2)
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('feels_like', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    pressure = weather_data.get('pressure', 1013)
    wind_speed = weather_data.get('wind_speed', 0)
    visibility = weather_data.get('visibility', 10)
    
    # 构建天气信息摘要
    weather_summary = {
        "城市": city,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%",
        "气压": f"{pressure} hPa",
        "风速": f"{wind_speed} m/s",
        "能见度": f"{visibility} km"
    }
    
    # 构建提示词
    image_prompt = f"城市{city}的天气景象，{weather_desc}，温度{temperature}度，体感{feels_like}度，{humidity}%湿度，气压{pressure}hPa"
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，体感温度{feels_like}度，湿度{humidity}%，气压{pressure}hPa"
    
    # 只返回最基本的字段，避免验证错误
    return {
        "weather_info": weather_summary,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        "city": city,
        "temperature": temperature,
        "weather_description": weather_desc,
        "humidity": humidity
    }
