#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import os

def test_openweather_directly():
    """直接测试OpenWeatherMap API"""
    print("测试OpenWeatherMap API...")
    
    api_key = "811a271ed44e1d5599d8e0c773417557"
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': 'Beijing',
            'appid': api_key,
            'units': 'metric',
            'lang': 'zh_cn'
        }
        
        response = requests.get(url, params=params, timeout=10)
        print(f"OpenWeatherMap API状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("OpenWeatherMap API调用成功!")
            print(f"城市: {data.get('name', 'N/A')}")
            print(f"温度: {data.get('main', {}).get('temp', 'N/A')}°C")
            print(f"体感温度: {data.get('main', {}).get('feels_like', 'N/A')}°C")
            print(f"天气: {data.get('weather', [{}])[0].get('description', 'N/A')}")
            print(f"湿度: {data.get('main', {}).get('humidity', 'N/A')}%")
            return True
        else:
            print(f"OpenWeatherMap API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"OpenWeatherMap API测试失败: {e}")
        return False

def test_local_api():
    """测试本地API"""
    print("\n测试本地API...")
    
    # 设置环境变量
    os.environ['WEATHER_API_KEY'] = "811a271ed44e1d5599d8e0c773417557"
    
    local_url = "http://localhost:8000"
    
    try:
        # 测试服务状态
        response = requests.get(f"{local_url}/", timeout=10)
        print(f"服务状态: {response.status_code}")
        print(f"响应: {response.json()}")
        
        # 测试天气查询
        params = {"city": "北京"}
        response = requests.get(f"{local_url}/weather", params=params, timeout=10)
        print(f"天气查询状态: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"API返回错误: {data['error']}")
                return False
            else:
                print("天气查询成功!")
                print(f"城市: {data.get('city', 'N/A')}")
                print(f"温度: {data.get('temperature', 'N/A')}°C")
                print(f"体感温度: {data.get('feels_like', 'N/A')}°C")
                print(f"天气: {data.get('description', 'N/A')}")
                print(f"湿度: {data.get('humidity', 'N/A')}%")
                return True
        else:
            print(f"天气查询失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"本地API测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试天气API...")
    
    # 首先测试OpenWeatherMap API
    openweather_ok = test_openweather_directly()
    
    if openweather_ok:
        print("\n" + "="*50)
        print("OpenWeatherMap API可用，现在测试本地服务...")
        print("请确保本地服务器正在运行: python main.py")
        print("="*50)
        
        # 测试本地API
        local_ok = test_local_api()
        
        if local_ok:
            print("\n所有测试通过!")
            print("API密钥配置正确")
            print("本地服务运行正常")
            print("天气查询功能正常")
            print("\n下一步:")
            print("1. 部署到Render")
            print("2. 在Render中设置环境变量 WEATHER_API_KEY")
            print("3. 在Dify中配置正确的API URL")
        else:
            print("\n本地服务测试失败")
            print("请检查:")
            print("1. 服务器是否正在运行 (python main.py)")
            print("2. 端口8000是否被占用")
    else:
        print("\nOpenWeatherMap API测试失败")
        print("请检查:")
        print("1. API密钥是否正确")
        print("2. 网络连接是否正常")
        print("3. API密钥是否已激活")
