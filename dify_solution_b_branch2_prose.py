#!/usr/bin/env python3
"""
方案B - 支路2：散文生成代码执行节点
生成散文提示词和上下文
"""

def main(*args, **kwargs):
    """
    支路2：散文生成节点
    支持位置参数和关键字参数，兼容Dify的调用方式
    输入：处理后的天气数据
    输出：散文提示词和上下文
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
    
    # 获取季节信息
    season = get_season_from_temperature(temperature)
    
    # 获取时间描述
    time_description = get_time_description()
    
    # 获取城市特色
    city_characteristics = get_city_characteristics(city)
    
    # 构建散文提示词
    prose_prompt = f"""
请为{city}这座城市写一段优美的散文，描述当前的天气状况。

【城市背景】
{city_characteristics}

【天气信息】
- 城市：{city}
- 时间：{time_description}
- 季节：{season}
- 温度：{temperature}°C
- 体感温度：{feels_like}°C
- 天气状况：{weather_description}
- 湿度：{humidity}%
- 气压：{pressure} hPa
- 风速：{wind_speed} m/s
- 能见度：{visibility} km

【写作要求】
1. 语言优美，富有诗意
2. 描写生动，画面感强
3. 情感真挚，引人共鸣
4. 字数控制在200-300字
5. 体现城市特色和天气氛围
6. 可以包含人物活动、城市景观、自然现象等元素

【写作风格】
- 散文体，语言流畅自然
- 适当使用修辞手法（比喻、拟人、排比等）
- 情感表达细腻，有温度
- 结构清晰，层次分明
    """
    
    # 构建散文上下文
    prose_context = f"""
城市：{city}
时间：{time_description}
季节：{season}
天气：{weather_description}
温度：{temperature}°C（体感{feels_like}°C）
湿度：{humidity}%
风速：{wind_speed}m/s
能见度：{visibility}km
    """
    
    # 构建散文指令
    prose_instruction = f"为{city}写一段关于{weather_description}天气的优美散文，体现{season}季节特色"
    
    # 构建散文风格描述
    prose_style = f"优美散文，富有诗意，体现{season}季节的{weather_description}天气氛围"
    
    # 构建关键词
    keywords = [
        city, weather_description, season, 
        f"{temperature}度", f"体感{feels_like}度",
        f"湿度{humidity}%", f"风速{wind_speed}m/s"
    ]
    
    return {
        "prose_prompt": prose_prompt,
        "prose_context": prose_context,
        "prose_instruction": prose_instruction,
        "prose_style": prose_style,
        "keywords": keywords,
        "season": season,
        "time_description": time_description,
        "city_characteristics": city_characteristics,
        "weather_mood": get_weather_mood(weather_description, temperature),
        "writing_tone": get_writing_tone(weather_description, temperature)
    }

def get_season_from_temperature(temperature):
    """根据温度判断季节"""
    if temperature < 5:
        return "严冬"
    elif temperature < 15:
        return "初冬" if temperature < 10 else "深秋"
    elif temperature < 25:
        return "春秋" if temperature < 20 else "初夏"
    elif temperature < 30:
        return "盛夏"
    else:
        return "酷夏"

def get_time_description():
    """获取时间描述"""
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    
    if 5 <= hour < 8:
        return "清晨"
    elif 8 <= hour < 12:
        return "上午"
    elif 12 <= hour < 14:
        return "中午"
    elif 14 <= hour < 18:
        return "下午"
    elif 18 <= hour < 20:
        return "傍晚"
    elif 20 <= hour < 23:
        return "夜晚"
    else:
        return "深夜"

def get_city_characteristics(city):
    """获取城市特色描述"""
    city_info = {
        "北京": "古都北京，有着深厚的历史文化底蕴，胡同巷陌间藏着老北京的味道",
        "上海": "魔都上海，现代与传统交融，外滩的繁华与弄堂的宁静相映成趣",
        "广州": "花城广州，四季如春，珠江两岸灯火辉煌，粤菜飘香",
        "深圳": "鹏城深圳，改革开放的前沿，年轻而充满活力",
        "杭州": "人间天堂杭州，西湖美景，江南水乡的温婉与诗意",
        "成都": "天府之国成都，悠闲的生活节奏，麻辣的川菜文化",
        "西安": "古都西安，十三朝古都，兵马俑见证着历史的厚重",
        "南京": "六朝古都南京，秦淮河畔，江南文人的风雅之地"
    }
    
    return city_info.get(city, f"{city}这座城市，有着独特的城市风貌和文化特色")

def get_weather_mood(weather_desc, temperature):
    """获取天气氛围"""
    mood_map = {
        "晴": "明媚阳光，心情愉悦",
        "多云": "云卷云舒，变化万千",
        "阴": "阴云密布，沉静内敛",
        "雨": "细雨绵绵，诗意盎然",
        "雪": "雪花纷飞，纯净美好",
        "雾": "雾气朦胧，神秘莫测",
        "霾": "雾霾笼罩，需要关注"
    }
    
    base_mood = mood_map.get(weather_desc, "天气变化，感受自然")
    
    if temperature < 10:
        return f"{base_mood}，寒意阵阵"
    elif temperature > 25:
        return f"{base_mood}，热浪滚滚"
    else:
        return f"{base_mood}，温度适宜"

def get_writing_tone(weather_desc, temperature):
    """获取写作基调"""
    if "雨" in weather_desc:
        return "诗意、浪漫、略带忧郁"
    elif "雪" in weather_desc:
        return "纯净、美好、宁静"
    elif "晴" in weather_desc:
        return "明亮、欢快、充满希望"
    elif "阴" in weather_desc:
        return "沉静、内敛、思考"
    elif temperature < 10:
        return "清冷、萧瑟、怀旧"
    elif temperature > 25:
        return "热烈、奔放、充满活力"
    else:
        return "温和、舒适、平和"
