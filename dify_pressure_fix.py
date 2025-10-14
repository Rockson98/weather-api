#!/usr/bin/env python3
"""
Dify代码执行节点 - 解决pressure missing错误
专门修复"Output pressure is missing"问题
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
    pressure = weather_data.get('pressure', 1013)  # 标准大气压，解决missing错误
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
    
    # 返回所有必要的输出字段，特别确保所有missing字段都存在
    return {
        # 核心字段 - 解决missing错误
        "weather_main": weather_summary,
        "pressure": pressure,  # 解决"Output pressure is missing"错误
        "generated_image_url": "",  # 解决"Output generated_image_url is missing"错误
        
        # 主要输出字段
        "weather_info": weather_summary,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        
        # 基础天气字段
        "city": city,
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "visibility": visibility,
        
        # 兼容性字段 - 防止其他missing错误
        "weather": weather_desc,
        "temp": temperature,
        "humidity_percent": humidity,
        "pressure_hpa": pressure,
        "wind": wind_speed,
        "vis": visibility,
        
        # 额外的天气字段
        "weather_condition": weather_desc,
        "feels_like_temp": feels_like,
        "wind_direction": weather_data.get('wind_direction', 0),
        "uv_index": weather_data.get('uv_index', 0),
        "cloud_cover": weather_data.get('cloud_cover', 0),
        
        # 图像相关字段 - 防止图像生成节点missing错误
        "image_url": "",
        "generated_image": "",
        "image_description": image_prompt,
        "image_prompt_text": image_prompt,
        
        # 文本生成相关字段 - 防止文本生成节点missing错误
        "generated_text": "",
        "prose_content": "",
        "generated_prose": "",
        "weather_poem": "",
        "weather_story": ""
    }
