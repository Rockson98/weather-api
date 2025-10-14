#!/usr/bin/env python3
"""
方案B - 主数据处理代码执行节点
处理天气API数据，为三个支路准备数据
"""

def main(*args, **kwargs):
    """
    主数据处理节点
    支持位置参数和关键字参数，兼容Dify的调用方式
    
    返回处理后的天气数据给三个支路
    """
    
    # 参数验证和默认值处理 - 支持多种参数传递方式
    weather_data = []
    city = "未知城市"
    
    # 处理位置参数
    if len(args) > 0:
        weather_data = args[0]
    if len(args) > 1:
        city = args[1]
    
    # 处理关键字参数
    if 'weather' in kwargs:
        weather_data = kwargs['weather']
    elif 'weather_data' in kwargs:
        weather_data = kwargs['weather_data']
    
    if 'city' in kwargs:
        city = kwargs['city']
    
    # 确保weather_data不为None
    if weather_data is None:
        weather_data = []
    
    # 处理天气数据 - 支持JSON数组格式
    debug_info = f"原始数据类型: {type(weather_data)}, 内容: {weather_data}"
    
    # 如果是数组，取第一个元素
    if isinstance(weather_data, list):
        if len(weather_data) > 0:
            weather_data = weather_data[0]
            debug_info += f" | 从数组中提取第一个元素: {weather_data}"
        else:
            weather_data = {}
            debug_info += " | 数组为空，使用默认值"
    
    # 确保是字典格式
    if not isinstance(weather_data, dict):
        weather_data = {}
        debug_info += " | 不是字典格式，使用默认值"
    
    # 提取天气信息，支持多种字段名格式
    city = weather_data.get('city', weather_data.get('name', city))
    
    # 温度字段映射
    temperature = weather_data.get('temperature', 
                                 weather_data.get('temp', 
                                 weather_data.get('main', {}).get('temp', 0)))
    
    # 体感温度字段映射
    feels_like = weather_data.get('feels_like', 
                                 weather_data.get('feels_like_temp',
                                 weather_data.get('main', {}).get('feels_like', 0)))
    
    # 天气描述字段映射
    weather_desc = weather_data.get('description', 
                                   weather_data.get('weather', [{}])[0].get('description', '') if weather_data.get('weather') else '')
    
    # 湿度字段映射
    humidity = weather_data.get('humidity', 
                               weather_data.get('main', {}).get('humidity', 0))
    
    # 气压字段映射
    pressure = weather_data.get('pressure', 
                               weather_data.get('main', {}).get('pressure', 1013))
    
    # 风速字段映射
    wind_speed = weather_data.get('wind_speed', 
                                 weather_data.get('wind', {}).get('speed', 0))
    
    # 能见度字段映射
    visibility = weather_data.get('visibility', 
                                 weather_data.get('vis', 10))
    
    # 添加调试信息
    debug_info += f" | 提取结果: 城市={city}, 温度={temperature}, 体感={feels_like}, 天气={weather_desc}"
    
    # 计算天气指数
    weather_index = calculate_weather_index(temperature, humidity, pressure, wind_speed)
    
    # 生成天气摘要
    weather_summary = f"{city}今日{weather_desc}，温度{temperature}°C，体感{feels_like}°C"
    
    # 返回处理后的数据 - 只返回Dify配置中必需的字段
    return {
        "city": str(city),
        "temperature": float(temperature),
        "feels_like": float(feels_like),
        "weather_description": str(weather_desc),
        "humidity": int(humidity),
        "pressure": int(pressure),
        "wind_speed": float(wind_speed),
        "visibility": int(visibility),
        "weather_summary": str(weather_summary),
        "weather_index": weather_index,
        "raw_weather_data": weather_data,
        "debug_info": str(debug_info)
    }

def calculate_weather_index(temperature, humidity, pressure, wind_speed):
    """计算天气指数"""
    # 温度指数 (0-100)
    temp_score = min(100, max(0, 50 + (temperature - 20) * 2))
    
    # 湿度指数 (0-100)
    humidity_score = min(100, max(0, 100 - abs(humidity - 50) * 2))
    
    # 气压指数 (0-100)
    pressure_score = min(100, max(0, 100 - abs(pressure - 1013) * 0.1))
    
    # 风速指数 (0-100)
    wind_score = min(100, max(0, 100 - wind_speed * 5))
    
    # 综合指数
    overall_score = (temp_score + humidity_score + pressure_score + wind_score) / 4
    
    return {
        "overall": round(overall_score, 1),
        "temperature": round(temp_score, 1),
        "humidity": round(humidity_score, 1),
        "pressure": round(pressure_score, 1),
        "wind": round(wind_score, 1)
    }

# 测试函数
def test_weather_data_processing():
    """测试天气数据处理功能"""
    
    # 模拟天气API返回的JSON数组格式
    test_weather_array = [
        {
            "city": "北京",
            "main": {
                "temp": 25.5,
                "feels_like": 28.0,
                "humidity": 65,
                "pressure": 1013
            },
            "weather": [
                {
                    "description": "多云"
                }
            ],
            "wind": {
                "speed": 3.2
            },
            "visibility": 10
        }
    ]
    
    # 测试处理
    result = main(test_weather_array, "北京")
    
    print("=== 天气数据处理测试 ===")
    print(f"调试信息: {result['debug_info']}")
    print(f"城市: {result['city']}")
    print(f"温度: {result['temperature']}")
    print(f"体感温度: {result['feels_like']}")
    print(f"天气描述: {result['weather_description']}")
    print(f"湿度: {result['humidity']}")
    print(f"气压: {result['pressure']}")
    print(f"风速: {result['wind_speed']}")
    print(f"能见度: {result['visibility']}")
    print(f"天气摘要: {result['weather_summary']}")
    
    return result

# 主函数调用
if __name__ == "__main__":
    test_weather_data_processing()
    
    # 测试无参数调用（模拟Dify调用）
    print("\n=== 测试无参数调用 ===")
    result = main()
    print(f"无参数调用结果: {result['city']}, {result['weather_summary']}")
