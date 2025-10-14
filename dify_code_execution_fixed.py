#!/usr/bin/env python3
"""
Dify代码执行节点 - 修复版本
解决 "Output weather_main is missing" 错误
"""

def main(arg1, arg2):
    """
    arg1: 天气API返回的数据（可能是列表或对象）
    arg2: 开始步骤输入的城市名称
    """
    
    # 1. 处理天气数据 - 确保是对象格式
    weather_data = arg1
    
    # 如果arg1是列表，取第一个元素
    if isinstance(weather_data, list) and len(weather_data) > 0:
        weather_data = weather_data[0]
    
    # 确保weather_data是字典
    if not isinstance(weather_data, dict):
        weather_data = {}
    
    # 提取天气信息
    city = weather_data.get('city', arg2)  # 优先使用API返回的城市名
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('feels_like', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    
    # 2. 构建用于LLM的天气信息摘要
    weather_summary = {
        "城市": city,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%"
    }
    
    # 3. 构建图片描述提示词
    image_prompt = f"城市{city}的天气景象，{weather_desc}，温度{temperature}度，体感{feels_like}度，{humidity}%湿度，{get_weather_mood(weather_desc, temperature)}"
    
    # 4. 构建散文描述提示词
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，体感温度{feels_like}度，湿度{humidity}%"
    
    # 5. 返回结构化数据供后续节点使用
    # 包含所有可能的输出字段，包括weather_main
    return {
        "weather_main": weather_summary,  # 添加这个字段解决错误
        "weather_info": weather_summary,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        "city": city,
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity
    }

def get_weather_mood(weather_desc, temperature):
    """根据天气状况生成情绪描述"""
    mood_map = {
        "晴": "阳光明媚，天空湛蓝",
        "多云": "云层密布，天空灰蒙",
        "雨": "细雨绵绵，空气清新",
        "雪": "雪花纷飞，银装素裹",
        "雾": "雾气朦胧，若隐若现",
        "阴": "阴云密布，略显沉闷"
    }
    
    for key, mood in mood_map.items():
        if key in weather_desc:
            return mood
    
    # 根据温度判断
    if temperature > 30:
        return "炎热干燥，阳光强烈"
    elif temperature > 20:
        return "温暖宜人，气候舒适"
    elif temperature > 10:
        return "凉爽清新，秋意盎然"
    else:
        return "寒冷刺骨，冬意浓浓"
