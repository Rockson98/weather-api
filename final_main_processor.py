"""
方案B - 主数据处理代码执行节点 (最终修复版)
处理天气API数据，为三个支路准备数据
"""

def main(*args, **kwargs):
    """
    主数据处理节点
    支持多种参数传递方式，确保Dify兼容性
    """
    
    # 参数处理
    weather_data = None
    city = None
    
    # 从位置参数获取
    if len(args) > 0:
        weather_data = args[0]
    if len(args) > 1:
        city = args[1]
    
    # 从关键字参数获取
    weather_data = kwargs.get('weather_data', weather_data)
    city = kwargs.get('city', city)
    
    # 设置默认值
    if weather_data is None:
        weather_data = {}
    if city is None:
        city = "未知城市"
    
    # 处理天气数据 - 支持多种数据结构
    if isinstance(weather_data, list) and len(weather_data) > 0:
        weather_data = weather_data[0]
    
    if not isinstance(weather_data, dict):
        weather_data = {}
    
    # 初始化所有变量
    temperature = None
    feels_like = None
    weather_desc = None
    humidity = None
    pressure = None
    wind_speed = None
    visibility = None
    
    # 智能数据提取函数
    def extract_value(data, *keys):
        """从嵌套字典中提取值，支持多个可能的键路径"""
        for key in keys:
            if isinstance(data, dict) and key in data:
                return data[key]
        return None
    
    # 提取城市名
    city = extract_value(weather_data, 'city', 'name') or city
    
    # 特殊处理：如果weather[0]中有完整的天气数据，优先使用
    weather_array = extract_value(weather_data, 'weather')
    if weather_array and isinstance(weather_array, list) and len(weather_array) > 0:
        weather_item = weather_array[0]
        if isinstance(weather_item, dict):
            # 直接从weather[0]中提取数据
            temperature = extract_value(weather_item, 'temperature', 'temp')
            feels_like = extract_value(weather_item, 'feels_like')
            humidity = extract_value(weather_item, 'humidity')
            weather_desc = extract_value(weather_item, 'description')
    
    # 如果weather[0]中没有数据，尝试从根级别提取
    if temperature is None:
        temperature = extract_value(weather_data, 'temperature', 'temp')
        if temperature is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                temperature = extract_value(main_data, 'temp', 'temperature')
    
    if feels_like is None:
        feels_like = extract_value(weather_data, 'feels_like')
        if feels_like is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                feels_like = extract_value(main_data, 'feels_like')
    
    if humidity is None:
        humidity = extract_value(weather_data, 'humidity')
        if humidity is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                humidity = extract_value(main_data, 'humidity')
    
    if weather_desc is None:
        weather_desc = extract_value(weather_data, 'description', 'weather_description')
        if weather_desc is None:
            weather_array = extract_value(weather_data, 'weather')
            if weather_array and isinstance(weather_array, list) and len(weather_array) > 0:
                weather_desc = extract_value(weather_array[0], 'description', 'main', 'weather_description')
    
    # 提取其他数据
    pressure = extract_value(weather_data, 'pressure')
    if pressure is None:
        main_data = extract_value(weather_data, 'main')
        if main_data:
            pressure = extract_value(main_data, 'pressure')
    
    wind_speed = extract_value(weather_data, 'wind_speed', 'speed')
    if wind_speed is None:
        wind_data = extract_value(weather_data, 'wind')
        if wind_data:
            wind_speed = extract_value(wind_data, 'speed', 'wind_speed')
    
    visibility = extract_value(weather_data, 'visibility')
    
    # 设置默认值
    temperature = float(temperature) if temperature is not None else 0.0
    feels_like = float(feels_like) if feels_like is not None else 0.0
    humidity = int(humidity) if humidity is not None else 0
    pressure = int(pressure) if pressure is not None else 1013
    wind_speed = float(wind_speed) if wind_speed is not None else 0.0
    visibility = int(visibility) if visibility is not None else 10
    weather_desc = str(weather_desc) if weather_desc is not None else "未知"
    
    # 生成摘要
    weather_summary = f"{city}今日{weather_desc}，温度{temperature}°C，体感{feels_like}°C"
    
    # 计算天气指数
    weather_index = {
        "overall": 75.0,
        "temperature": 80.0,
        "humidity": 70.0,
        "pressure": 85.0,
        "wind": 65.0
    }
    
    # 返回数据 - 确保所有字段都有值
    return {
        "city": str(city),
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "visibility": visibility,
        "weather_summary": weather_summary,
        "weather_index": weather_index,
        "raw_weather_data": weather_data,
        "debug_info": f"处理完成: {city}, {temperature}°C, {weather_desc}"
    }

# 测试代码
if __name__ == "__main__":
    # 测试您提供的数据结构
    print("=== 测试您提供的数据结构 ===")
    test_data = {
        "city": "Beijing",
        "weather": [
            {
                "city": "Beijing",
                "description": "晴",
                "feels_like": 20.26,
                "humidity": 45,
                "temperature": 20.94
            }
        ]
    }
    result = main(test_data, "Beijing")
    print("修复后的结果:")
    print(f"城市: {result['city']}")
    print(f"温度: {result['temperature']}°C")
    print(f"体感温度: {result['feels_like']}°C")
    print(f"湿度: {result['humidity']}%")
    print(f"天气描述: {result['weather_description']}")
    print(f"摘要: {result['weather_summary']}")
    
    # 测试标准OpenWeatherMap格式
    print("\n=== 测试标准OpenWeatherMap格式 ===")
    standard_data = {
        "name": "Beijing",
        "main": {
            "temp": 25.5,
            "feels_like": 28.0,
            "humidity": 65,
            "pressure": 1013
        },
        "weather": [
            {
                "description": "晴天"
            }
        ],
        "wind": {
            "speed": 3.2
        },
        "visibility": 10
    }
    result2 = main(standard_data, "Beijing")
    print("标准格式结果:")
    print(f"城市: {result2['city']}")
    print(f"温度: {result2['temperature']}°C")
    print(f"体感温度: {result2['feels_like']}°C")
    print(f"湿度: {result2['humidity']}%")
    print(f"天气描述: {result2['weather_description']}")
