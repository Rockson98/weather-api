#!/usr/bin/env python3
"""
天气API测试脚本
用于测试本地和远程API的功能
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_api(base_url, api_key=None):
    """测试API功能"""
    print(f"\n🔍 测试API: {base_url}")
    print("=" * 50)
    
    # 测试1: 服务状态
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ 服务状态: {response.status_code}")
        print(f"📄 响应: {response.json()}")
    except Exception as e:
        print(f"❌ 服务状态测试失败: {e}")
        return False
    
    # 测试2: OpenAPI文档
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        print(f"✅ OpenAPI文档: {response.status_code}")
        if response.status_code == 200:
            openapi_data = response.json()
            print(f"📄 API标题: {openapi_data.get('info', {}).get('title', 'N/A')}")
    except Exception as e:
        print(f"❌ OpenAPI文档测试失败: {e}")
    
    # 测试3: 天气查询
    try:
        params = {"city": "北京"}
        response = requests.get(f"{base_url}/weather", params=params, timeout=10)
        print(f"✅ 天气查询: {response.status_code}")
        print(f"📄 响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"⚠️  API返回错误: {data['error']}")
                if "API密钥未配置" in data['error']:
                    print("💡 解决方案: 需要在环境变量中设置 WEATHER_API_KEY")
            else:
                print("🎉 天气查询成功!")
                return True
        else:
            print(f"❌ 天气查询失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 天气查询测试失败: {e}")
    
    return False

def main():
    """主函数"""
    print("🌤️  天气API测试工具")
    print("=" * 50)
    
    # 获取API密钥
    api_key = os.getenv('WEATHER_API_KEY')
    if api_key:
        print(f"🔑 检测到API密钥: {api_key[:8]}...")
    else:
        print("⚠️  未检测到API密钥 (WEATHER_API_KEY)")
        print("💡 请在.env文件中设置您的OpenWeatherMap API密钥")
    
    # 测试本地API
    local_url = "http://localhost:8000"
    print(f"\n🏠 测试本地API...")
    local_success = test_api(local_url, api_key)
    
    # 测试远程API (请替换为您的实际Render URL)
    remote_url = "https://your-app-name.onrender.com"  # 请替换为您的实际URL
    print(f"\n🌐 测试远程API...")
    print(f"⚠️  请将 {remote_url} 替换为您的实际Render URL")
    
    # 总结
    print("\n📊 测试总结")
    print("=" * 50)
    if local_success:
        print("✅ 本地API测试通过")
    else:
        print("❌ 本地API测试失败")
        print("💡 请检查:")
        print("   1. 服务器是否正在运行 (python main.py)")
        print("   2. API密钥是否正确设置")
        print("   3. 网络连接是否正常")
    
    print("\n🔧 下一步操作:")
    print("1. 如果本地测试通过，请部署到Render")
    print("2. 在Render中设置环境变量 WEATHER_API_KEY")
    print("3. 在Dify中使用正确的API URL")

if __name__ == "__main__":
    main()
