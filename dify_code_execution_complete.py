#!/usr/bin/env python3
"""
Dify代码执行节点 - 完整版本
包含所有可能的天气字段，解决所有missing错误
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
    
    # 提取所有可能的天气信息
    city = weather_data.get('city', arg2)
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('feels_like', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    pressure = weather_data.get('pressure', 1013)  # 添加pressure字段
    wind_speed = weather_data.get('wind_speed', 0)
    wind_direction = weather_data.get('wind_direction', 0)
    visibility = weather_data.get('visibility', 10)
    uv_index = weather_data.get('uv_index', 0)
    cloud_cover = weather_data.get('cloud_cover', 0)
    
    # 构建天气信息摘要
    weather_summary = {
        "城市": city,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%",
        "气压": f"{pressure} hPa",
        "风速": f"{wind_speed} m/s",
        "能见度": f"{visibility} km",
        "紫外线指数": uv_index,
        "云量": f"{cloud_cover}%"
    }
    
    # 构建提示词
    image_prompt = f"城市{city}的天气景象，{weather_desc}，温度{temperature}度，体感{feels_like}度，{humidity}%湿度，气压{pressure}hPa"
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，体感温度{feels_like}度，湿度{humidity}%，气压{pressure}hPa"
    
    # 返回完整输出，包含所有可能的字段
    return {
        # 主要输出字段
        "weather_main": weather_summary,
        "weather_info": weather_summary,
        
        # 提示词字段
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        
        # 基础天气字段
        "city": city,
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity,
        
        # 扩展天气字段
        "pressure": pressure,  # 解决pressure missing错误
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
        "visibility": visibility,
        "uv_index": uv_index,
        "cloud_cover": cloud_cover,
        
        # 兼容性字段
        "weather": weather_desc,
        "temp": temperature,
        "feels_like_temp": feels_like,
        "weather_condition": weather_desc,
        "humidity_percent": humidity,
        "pressure_hpa": pressure,
        "wind": wind_speed,
        "wind_dir": wind_direction,
        "vis": visibility,
        "uv": uv_index,
        "clouds": cloud_cover
    }
