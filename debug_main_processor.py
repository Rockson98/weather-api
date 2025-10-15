"""
调试版本 - 主数据处理代码执行节点
用于诊断数据流问题
"""

def main(*args, **kwargs):
    """
    调试版本的主数据处理节点
    详细记录所有输入参数和数据流
    """
    
    # 详细记录所有输入参数
    debug_info = []
    debug_info.append("=== 调试信息开始 ===")
    debug_info.append(f"位置参数数量: {len(args)}")
    debug_info.append(f"关键字参数数量: {len(kwargs)}")
    
    # 记录位置参数
    for i, arg in enumerate(args):
        debug_info.append(f"位置参数[{i}]: {type(arg)} = {arg}")
    
    # 记录关键字参数
    for key, value in kwargs.items():
        debug_info.append(f"关键字参数[{key}]: {type(value)} = {value}")
    
    # 参数处理
    weather_data = None
    city = None
    
    # 从位置参数获取
    if len(args) > 0:
        weather_data = args[0]
        debug_info.append(f"从位置参数获取weather_data: {type(weather_data)} = {weather_data}")
    if len(args) > 1:
        city = args[1]
        debug_info.append(f"从位置参数获取city: {type(city)} = {city}")
    
    # 从关键字参数获取
    if 'weather_data' in kwargs:
        weather_data = kwargs['weather_data']
        debug_info.append(f"从关键字参数获取weather_data: {type(weather_data)} = {weather_data}")
    if 'city' in kwargs:
        city = kwargs['city']
        debug_info.append(f"从关键字参数获取city: {type(city)} = {city}")
    
    # 设置默认值
    if weather_data is None:
        weather_data = {}
        debug_info.append("weather_data为None，设置为空字典")
    if city is None:
        city = "未知城市"
        debug_info.append("city为None，设置为默认值")
    
    debug_info.append(f"最终weather_data: {type(weather_data)} = {weather_data}")
    debug_info.append(f"最终city: {type(city)} = {city}")
    
    # 处理天气数据 - 支持多种数据结构
    if isinstance(weather_data, list) and len(weather_data) > 0:
        debug_info.append(f"weather_data是列表，取第一个元素: {weather_data[0]}")
        weather_data = weather_data[0]
    
    if not isinstance(weather_data, dict):
        debug_info.append(f"weather_data不是字典类型: {type(weather_data)}")
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
                debug_info.append(f"找到键 '{key}': {data[key]}")
                return data[key]
        debug_info.append(f"未找到键: {keys}")
        return None
    
    # 提取城市名
    original_city = city
    city = extract_value(weather_data, 'city', 'name') or city
    if city != original_city:
        debug_info.append(f"从数据中提取城市名: {original_city} -> {city}")
    
    # 特殊处理：如果weather[0]中有完整的天气数据，优先使用
    weather_array = extract_value(weather_data, 'weather')
    if weather_array and isinstance(weather_array, list) and len(weather_array) > 0:
        debug_info.append(f"找到weather数组，长度: {len(weather_array)}")
        weather_item = weather_array[0]
        if isinstance(weather_item, dict):
            debug_info.append(f"weather[0]内容: {weather_item}")
            # 直接从weather[0]中提取数据
            temperature = extract_value(weather_item, 'temperature', 'temp')
            feels_like = extract_value(weather_item, 'feels_like')
            humidity = extract_value(weather_item, 'humidity')
            weather_desc = extract_value(weather_item, 'description')
    
    # 如果weather[0]中没有数据，尝试从根级别提取
    if temperature is None:
        debug_info.append("从根级别提取温度")
        temperature = extract_value(weather_data, 'temperature', 'temp')
        if temperature is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                debug_info.append(f"从main对象提取温度: {main_data}")
                temperature = extract_value(main_data, 'temp', 'temperature')
    
    if feels_like is None:
        debug_info.append("从根级别提取体感温度")
        feels_like = extract_value(weather_data, 'feels_like')
        if feels_like is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                feels_like = extract_value(main_data, 'feels_like')
    
    if humidity is None:
        debug_info.append("从根级别提取湿度")
        humidity = extract_value(weather_data, 'humidity')
        if humidity is None:
            main_data = extract_value(weather_data, 'main')
            if main_data:
                humidity = extract_value(main_data, 'humidity')
    
    if weather_desc is None:
        debug_info.append("从根级别提取天气描述")
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
    
    debug_info.append(f"最终提取结果: 温度={temperature}, 体感={feels_like}, 湿度={humidity}, 描述={weather_desc}")
    
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
    
    debug_info.append("=== 调试信息结束 ===")
    
    # 返回数据 - 包含详细的调试信息
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
        "debug_info": "\n".join(debug_info),
        "input_args_count": len(args),
        "input_kwargs_count": len(kwargs),
        "input_args": list(args),
        "input_kwargs": dict(kwargs)
    }
