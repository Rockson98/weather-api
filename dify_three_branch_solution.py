#!/usr/bin/env python3
"""
Dify三条独立支路工作流 - 完整解决方案
支路1: 天气播报 | 支路2: 散文生成 | 支路3: 图片生成
"""

def main(arg1, arg2):
    """
    arg1: 天气API返回的数据
    arg2: 城市名称
    
    返回三个支路所需的数据结构
    """
    
    # 处理天气数据
    weather_data = arg1
    if isinstance(weather_data, list) and len(weather_data) > 0:
        weather_data = weather_data[0]
    if not isinstance(weather_data, dict):
        weather_data = {}
    
    # 提取天气信息，确保所有字段都有默认值
    city = weather_data.get('city', arg2)
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('feels_like', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    pressure = weather_data.get('pressure', 1013)
    wind_speed = weather_data.get('wind_speed', 0)
    visibility = weather_data.get('visibility', 10)
    
    # ==================== 支路1: 天气播报 ====================
    weather_broadcast = {
        "城市": city,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%",
        "气压": f"{pressure} hPa",
        "风速": f"{wind_speed} m/s",
        "能见度": f"{visibility} km"
    }
    
    # ==================== 支路2: 散文生成 ====================
    prose_prompt = f"""
    请为{city}这座城市写一段优美的散文，描述当前的天气状况。
    
    天气信息：
    - 城市：{city}
    - 温度：{temperature}°C
    - 体感温度：{feels_like}°C
    - 天气状况：{weather_desc}
    - 湿度：{humidity}%
    - 气压：{pressure} hPa
    - 风速：{wind_speed} m/s
    - 能见度：{visibility} km
    
    请用优美的语言描述这座城市在这样天气下的景象和氛围，可以包含：
    1. 城市景观的描写
    2. 天气对城市氛围的影响
    3. 人们在这种天气下的感受
    4. 季节感和时间感
    """
    
    prose_context = f"城市：{city}，天气：{weather_desc}，温度：{temperature}°C，体感：{feels_like}°C"
    
    # ==================== 支路3: 图片生成 ====================
    image_prompt = f"""
    A beautiful weather scene in {city} city, {weather_desc}, 
    temperature {temperature}°C, feels like {feels_like}°C, 
    humidity {humidity}%, atmospheric pressure {pressure}hPa, 
    wind speed {wind_speed}m/s, visibility {visibility}km, 
    realistic photography style, high quality, detailed, 
    urban landscape, weather atmosphere, natural lighting
    """
    
    image_description = f"{city}的{weather_desc}天气景象，温度{temperature}°C，体感{feels_like}°C"
    
    # ==================== 返回三个支路的数据 ====================
    return {
        # 支路1: 天气播报数据
        "weather_broadcast": weather_broadcast,
        "weather_info": weather_broadcast,
        "city": city,
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "visibility": visibility,
        
        # 支路2: 散文生成数据
        "prose_prompt": prose_prompt,
        "prose_context": prose_context,
        "prose_instruction": f"为{city}写一段关于{weather_desc}天气的优美散文",
        "prose_style": "优美散文，富有诗意",
        
        # 支路3: 图片生成数据
        "image_prompt": image_prompt,
        "image_description": image_description,
        "image_style": "realistic photography",
        "image_quality": "high quality, detailed",
        "image_subject": f"{city} weather scene"
    }
