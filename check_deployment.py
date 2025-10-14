#!/usr/bin/env python3
"""
部署检查脚本
检查API服务是否正常运行
"""

import requests
import json
import sys

def check_api_health(url):
    """检查API服务健康状态"""
    try:
        # 检查根路径
        response = requests.get(f"{url}/", timeout=10)
        if response.status_code == 200:
            print("✅ API服务根路径正常")
        else:
            print(f"⚠️  API服务根路径返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法访问API服务根路径: {e}")
        return False
    
    try:
        # 检查OpenAPI文档
        response = requests.get(f"{url}/openapi.json", timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI文档可访问")
            try:
                openapi_data = response.json()
                print(f"   API标题: {openapi_data.get('info', {}).get('title', 'N/A')}")
                print(f"   API版本: {openapi_data.get('info', {}).get('version', 'N/A')}")
            except:
                print("   ⚠️  OpenAPI文档格式可能有问题")
        else:
            print(f"❌ OpenAPI文档返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法访问OpenAPI文档: {e}")
        return False
    
    try:
        # 测试天气API
        response = requests.get(f"{url}/weather?city=北京", timeout=10)
        if response.status_code == 200:
            print("✅ 天气API测试成功")
            try:
                weather_data = response.json()
                print(f"   测试城市: {weather_data.get('city', 'N/A')}")
                print(f"   温度: {weather_data.get('temperature', 'N/A')}°C")
                print(f"   天气: {weather_data.get('description', 'N/A')}")
            except:
                print("   ⚠️  天气API响应格式可能有问题")
        else:
            print(f"❌ 天气API返回状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {error_data.get('error', 'N/A')}")
            except:
                print(f"   响应内容: {response.text}")
    except Exception as e:
        print(f"❌ 天气API测试失败: {e}")
        return False
    
    return True

def main():
    if len(sys.argv) != 2:
        print("使用方法: python check_deployment.py <部署URL>")
        print("示例: python check_deployment.py https://weather-api-xxxx.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"正在检查API服务: {url}")
    print("-" * 50)
    
    if check_api_health(url):
        print("\n🎉 API服务检查通过！可以集成到Dify中。")
        print(f"\n在Dify中使用以下URL添加工具:")
        print(f"{url}/openapi.json")
    else:
        print("\n❌ API服务检查失败，请检查部署状态。")
        sys.exit(1)

if __name__ == "__main__":
    main()
