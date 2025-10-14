#!/usr/bin/env python3
"""
Dify代码执行节点 - 修复版本
解决"raw_weather_data is not an object"错误
"""

def main(arg1, arg2):
    """
    Dify工作流代码执行节点 - 修复版本
    
    Args:
        arg1: 天气API返回的数据（可能是列表或对象）
        arg2: 开始步骤输入的城市名称
    
    Returns:
        包含处理后的天气信息的字典
    """
    
    print(f"Debug - arg1 type: {type(arg1)}")
    print(f"Debug - arg1 content: {arg1}")
    print(f"Debug - arg2: {arg2}")
    
    # 1. 处理天气数据 - 确保是对象格式
    weather_data = arg1
    
    # 如果arg1是列表，取第一个元素
    if isinstance(weather_data, list):
        print(f"Warning - arg1 is list, length: {len(weather_data)}")
        if len(weather_data) > 0:
            weather_data = weather_data[0]
            print(f"Success - take first element: {weather_data}")
        else:
            print("Error - list is empty, use default")
            weather_data = {}
    
    # 确保weather_data是字典
    if not isinstance(weather_data, dict):
        print(f"Warning - weather_data is not dict, type: {type(weather_data)}")
        weather_data = {}
    
    print(f"Success - final weather_data: {weather_data}")
    
    # 2. 提取天气信息
    city = weather_data.get('city', arg2)  # 优先使用API返回的城市名
    temperature = weather_data.get('temperature', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    
    print(f"Data extracted - city: {city}, temp: {temperature}, weather: {weather_desc}, humidity: {humidity}")
    
    # 3. 构建用于LLM的天气信息摘要
    weather_summary = {
        "城市": city,
        "温度": f"{temperature}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%"
    }
    
    # 4. 构建图片描述提示词
    image_prompt = f"城市{city}的天气景象，{weather_desc}，温度{temperature}度，{humidity}%湿度，{get_weather_mood(weather_desc, temperature)}"
    
    # 5. 构建散文描述提示词
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，湿度{humidity}%"
    
    # 6. 构建天气信息摘要文本
    weather_summary_text = f"""{city}天气信息：
城市：{city}
温度：{temperature}°C
天气：{weather_desc}
湿度：{humidity}%"""
    
    # 7. 返回结构化数据供后续节点使用
    result = {
        "weather_info": weather_summary,
        "weather_summary_text": weather_summary_text,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        "city": city,
        "temperature": temperature,
        "weather_description": weather_desc,
        "humidity": humidity,
        "raw_weather_data": weather_data  # 确保这是字典
    }
    
    print(f"Success - return result: {result}")
    return result

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
        return "凉爽宜人，气候温和"
    else:
        return "寒冷刺骨，需要保暖"

# 测试函数
if __name__ == "__main__":
    # 模拟测试数据
    test_data_list = [{"city": "北京", "temperature": 16.94, "description": "晴", "humidity": 56}]
    test_data_dict = {"city": "北京", "temperature": 16.94, "description": "晴", "humidity": 56}
    
    print("测试列表格式:")
    result1 = main(test_data_list, "北京")
    
    print("\n测试字典格式:")
    result2 = main(test_data_dict, "北京")
