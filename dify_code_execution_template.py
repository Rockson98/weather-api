def main(arg1, arg2):
    """
    Dify工作流代码执行节点模板
    arg1: 天气API返回的数据
    arg2: 开始步骤输入的城市名称
    """
    
    # 1. 解析天气API数据
    weather_data = arg1
    
    # 提取关键信息
    city = weather_data.get('city', arg2)
    temperature = weather_data.get('temperature', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    
    # 2. 构建图片描述提示词
    image_prompt = f"Beautiful cityscape of {city}, {weather_desc}, temperature {temperature}°C, {humidity}% humidity, {get_weather_mood(weather_desc, temperature)}"
    
    # 3. 构建散文描述提示词
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，湿度{humidity}%"
    
    # 4. 构建天气信息摘要
    weather_summary = f"城市：{city}\n温度：{temperature}°C\n天气：{weather_desc}\n湿度：{humidity}%"
    
    # 5. 返回结果
    return {
        "city": city,
        "temperature": temperature,
        "weather_description": weather_desc,
        "humidity": humidity,
        "weather_summary": weather_summary,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        "raw_data": weather_data
    }

def get_weather_mood(weather_desc, temperature):
    """根据天气状况生成情绪描述"""
    if "晴" in weather_desc or "sunny" in weather_desc.lower():
        return "sunny and bright"
    elif "雨" in weather_desc or "rain" in weather_desc.lower():
        return "rainy and fresh"
    elif "雪" in weather_desc or "snow" in weather_desc.lower():
        return "snowy and peaceful"
    elif "云" in weather_desc or "cloud" in weather_desc.lower():
        return "cloudy and atmospheric"
    elif temperature > 30:
        return "hot and sunny"
    elif temperature < 10:
        return "cold and crisp"
    else:
        return "pleasant and comfortable"
