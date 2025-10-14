#!/usr/bin/env python3
"""
方案B - 支路1：天气播报代码执行节点
生成格式化的天气播报内容
"""

from datetime import datetime

def main(*args, **kwargs):
    """
    支路1：天气播报节点
    支持位置参数和关键字参数，兼容Dify的调用方式
    输入：处理后的天气数据
    输出：格式化的天气播报
    """
    
    # 处理位置参数
    city = ""
    temperature = 0
    feels_like = 0
    weather_description = ""
    humidity = 0
    pressure = 1013
    wind_speed = 0
    visibility = 10
    
    if len(args) > 0:
        city = args[0] or ""
    if len(args) > 1:
        temperature = args[1] or 0
    if len(args) > 2:
        feels_like = args[2] or 0
    if len(args) > 3:
        weather_description = args[3] or ""
    if len(args) > 4:
        humidity = args[4] or 0
    if len(args) > 5:
        pressure = args[5] or 1013
    if len(args) > 6:
        wind_speed = args[6] or 0
    if len(args) > 7:
        visibility = args[7] or 10
    
    # 处理关键字参数（覆盖位置参数）
    city = kwargs.get('city', city)
    temperature = kwargs.get('temperature', temperature)
    feels_like = kwargs.get('feels_like', feels_like)
    weather_description = kwargs.get('weather_description', weather_description)
    humidity = kwargs.get('humidity', humidity)
    pressure = kwargs.get('pressure', pressure)
    wind_speed = kwargs.get('wind_speed', wind_speed)
    visibility = kwargs.get('visibility', visibility)
    
    # 获取当前时间
    current_time = datetime.now()
    time_str = current_time.strftime('%Y年%m月%d日 %H:%M')
    weekday = current_time.strftime('%A')
    
    # 天气图标映射
    weather_icons = {
        '晴': '☀️',
        '多云': '⛅',
        '阴': '☁️',
        '雨': '🌧️',
        '雪': '❄️',
        '雾': '🌫️',
        '霾': '😷',
        '雷': '⛈️'
    }
    
    # 获取天气图标
    weather_icon = weather_icons.get(weather_description, '🌤️')
    
    # 温度感受描述
    temp_feeling = get_temperature_feeling(temperature)
    
    # 湿度描述
    humidity_desc = get_humidity_description(humidity)
    
    # 风速描述
    wind_desc = get_wind_description(wind_speed)
    
    # 能见度描述
    visibility_desc = get_visibility_description(visibility)
    
    # 生成天气播报
    weather_broadcast = f"""
🌤️ {city}天气播报
📅 {time_str} {weekday}

{weather_icon} 天气状况：{weather_description}
🌡️ 温度：{temperature}°C ({temp_feeling})
🤔 体感温度：{feels_like}°C
💧 湿度：{humidity}% ({humidity_desc})
📊 气压：{pressure} hPa
💨 风速：{wind_speed} m/s ({wind_desc})
👁️ 能见度：{visibility} km ({visibility_desc})

💡 温馨提示：
{get_weather_tips(temperature, weather_description, humidity, wind_speed)}
    """
    
    # 生成简短摘要
    short_summary = f"{city}今日{weather_description}，温度{temperature}°C，体感{feels_like}°C"
    
    # 生成详细报告
    detailed_report = {
        "城市": city,
        "时间": time_str,
        "天气": weather_description,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "湿度": f"{humidity}%",
        "气压": f"{pressure} hPa",
        "风速": f"{wind_speed} m/s",
        "能见度": f"{visibility} km"
    }
    
    return {
        "weather_broadcast": weather_broadcast,
        "short_summary": short_summary,
        "detailed_report": detailed_report,
        "weather_icon": weather_icon,
        "temperature_feeling": temp_feeling,
        "humidity_description": humidity_desc,
        "wind_description": wind_desc,
        "visibility_description": visibility_desc,
        "weather_tips": get_weather_tips(temperature, weather_description, humidity, wind_speed)
    }

def get_temperature_feeling(temperature):
    """获取温度感受描述"""
    if temperature < 0:
        return "极寒"
    elif temperature < 5:
        return "严寒"
    elif temperature < 10:
        return "寒冷"
    elif temperature < 15:
        return "较冷"
    elif temperature < 20:
        return "凉爽"
    elif temperature < 25:
        return "舒适"
    elif temperature < 30:
        return "温暖"
    elif temperature < 35:
        return "炎热"
    else:
        return "酷热"

def get_humidity_description(humidity):
    """获取湿度描述"""
    if humidity < 30:
        return "干燥"
    elif humidity < 50:
        return "较干"
    elif humidity < 70:
        return "适宜"
    elif humidity < 80:
        return "较湿"
    else:
        return "潮湿"

def get_wind_description(wind_speed):
    """获取风速描述"""
    if wind_speed < 1:
        return "无风"
    elif wind_speed < 3:
        return "微风"
    elif wind_speed < 6:
        return "轻风"
    elif wind_speed < 10:
        return "和风"
    elif wind_speed < 15:
        return "清风"
    else:
        return "强风"

def get_visibility_description(visibility):
    """获取能见度描述"""
    if visibility < 1:
        return "极差"
    elif visibility < 3:
        return "很差"
    elif visibility < 5:
        return "较差"
    elif visibility < 10:
        return "一般"
    elif visibility < 20:
        return "良好"
    else:
        return "极佳"

def get_weather_tips(temperature, weather_desc, humidity, wind_speed):
    """获取天气温馨提示"""
    tips = []
    
    # 温度提示
    if temperature < 5:
        tips.append("天气寒冷，请注意保暖，建议穿厚外套")
    elif temperature > 30:
        tips.append("天气炎热，请注意防暑降温，多喝水")
    
    # 天气提示
    if "雨" in weather_desc:
        tips.append("有降雨，请携带雨具")
    elif "雪" in weather_desc:
        tips.append("有降雪，请注意路面湿滑")
    elif "雾" in weather_desc or "霾" in weather_desc:
        tips.append("能见度较低，请注意交通安全")
    
    # 湿度提示
    if humidity > 80:
        tips.append("湿度较高，注意防潮")
    elif humidity < 30:
        tips.append("空气干燥，注意保湿")
    
    # 风速提示
    if wind_speed > 10:
        tips.append("风力较大，注意安全")
    
    return "；".join(tips) if tips else "天气适宜，祝您愉快！"
