#!/usr/bin/env python3
"""
Dify集成问题诊断脚本
帮助解决"invalid schema"错误
"""

import requests
import json
import sys

def diagnose_url_issue(url):
    """诊断URL相关问题"""
    print(f"🔍 诊断URL: {url}")
    print("-" * 50)
    
    # 1. 检查URL格式
    print("1️⃣ 检查URL格式...")
    if not url.startswith(('http://', 'https://')):
        print("❌ 错误: URL必须以 http:// 或 https:// 开头")
        return False
    else:
        print("✅ URL格式正确")
    
    # 2. 检查根路径
    print("\n2️⃣ 检查服务根路径...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ 服务根路径正常")
        else:
            print(f"⚠️  服务根路径返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法访问服务根路径: {e}")
        return False
    
    # 3. 检查OpenAPI文档
    print("\n3️⃣ 检查OpenAPI文档...")
    openapi_url = f"{url}/openapi.json"
    try:
        response = requests.get(openapi_url, timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI文档可访问")
            
            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                print("✅ 内容类型正确 (application/json)")
            else:
                print(f"⚠️  内容类型: {content_type}")
            
            # 验证JSON格式
            try:
                data = response.json()
                print("✅ JSON格式有效")
                
                # 检查必需字段
                required_fields = ['openapi', 'info', 'paths']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"❌ 缺少必需字段: {missing_fields}")
                    return False
                else:
                    print("✅ 包含所有必需字段")
                
                # 检查OpenAPI版本
                openapi_version = data.get('openapi', '')
                if openapi_version.startswith('3.'):
                    print(f"✅ OpenAPI版本: {openapi_version}")
                else:
                    print(f"⚠️  OpenAPI版本: {openapi_version} (建议使用3.x)")
                
                # 检查路径
                paths = data.get('paths', {})
                if '/weather' in paths:
                    print("✅ 包含天气API路径")
                else:
                    print("❌ 缺少天气API路径")
                    return False
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析错误: {e}")
                return False
        else:
            print(f"❌ OpenAPI文档返回状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ 无法访问OpenAPI文档: {e}")
        return False

def test_weather_api(url):
    """测试天气API"""
    print("\n4️⃣ 测试天气API...")
    try:
        weather_url = f"{url}/weather?city=北京"
        response = requests.get(weather_url, timeout=10)
        if response.status_code == 200:
            print("✅ 天气API测试成功")
            try:
                data = response.json()
                print(f"   城市: {data.get('city', 'N/A')}")
                print(f"   温度: {data.get('temperature', 'N/A')}°C")
            except:
                print("   ⚠️  响应格式可能有问题")
        else:
            print(f"❌ 天气API返回状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ 天气API测试失败: {e}")

def main():
    print("🩺 Dify集成问题诊断工具")
    print("=" * 40)
    
    if len(sys.argv) != 2:
        print("使用方法: python diagnose_dify_issue.py <您的部署URL>")
        print("示例: python diagnose_dify_issue.py https://weather-api-xxxx.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 移除末尾斜杠
    if url.endswith('/'):
        url = url[:-1]
    
    # 诊断问题
    if diagnose_url_issue(url):
        print("\n🎉 诊断完成 - 所有检查通过！")
        print("\n📋 在Dify中使用以下配置:")
        print(f"工具名称: 天气查询工具")
        print(f"API文档URL: {url}/openapi.json")
        print(f"认证类型: 无认证")
        
        # 测试天气API
        test_weather_api(url)
        
        print("\n如果仍然出现'invalid schema'错误，可能是Dify的缓存问题，请:")
        print("1. 等待几分钟后重试")
        print("2. 清除浏览器缓存")
        print("3. 尝试使用不同的浏览器")
    else:
        print("\n❌ 诊断发现问题，请根据上述错误信息进行修复")

if __name__ == "__main__":
    main()
