#!/usr/bin/env python3
"""
修复Dify URL配置脚本
解决"invalid schema"错误
"""

import json
import sys
import requests

def validate_url(url):
    """验证URL格式"""
    if not url.startswith(('http://', 'https://')):
        print("❌ URL必须以 http:// 或 https:// 开头")
        return False
    
    if not url.endswith('.onrender.com'):
        print("⚠️  警告: URL似乎不是Render部署地址")
    
    return True

def test_openapi_endpoint(url):
    """测试OpenAPI端点是否可访问"""
    try:
        openapi_url = f"{url}/openapi.json"
        print(f"🧪 测试OpenAPI端点: {openapi_url}")
        
        response = requests.get(openapi_url, timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI端点可访问")
            
            # 验证JSON格式
            try:
                data = response.json()
                if 'openapi' in data and 'paths' in data:
                    print("✅ OpenAPI文档格式正确")
                    return True
                else:
                    print("❌ OpenAPI文档格式不正确")
                    return False
            except json.JSONDecodeError:
                print("❌ OpenAPI文档不是有效的JSON")
                return False
        else:
            print(f"❌ OpenAPI端点返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问OpenAPI端点: {e}")
        return False

def update_openapi_config(url):
    """更新OpenAPI配置文件"""
    print(f"🔧 更新OpenAPI配置: {url}")
    
    # 移除末尾的斜杠
    if url.endswith('/'):
        url = url[:-1]
    
    # 更新 openapi.json
    openapi_path = "dify_tool/openapi.json"
    try:
        with open(openapi_path, 'r', encoding='utf-8') as f:
            openapi = json.load(f)
        
        # 更新服务器URL
        openapi['servers'] = [
            {
                "url": url,
                "description": "Render生产服务器"
            }
        ]
        
        with open(openapi_path, 'w', encoding='utf-8') as f:
            json.dump(openapi, f, ensure_ascii=False, indent=2)
        
        print("✅ 已更新 openapi.json")
        return True
    except Exception as e:
        print(f"❌ 更新openapi.json失败: {e}")
        return False

def main():
    print("🔧 Dify URL配置修复工具")
    print("=" * 40)
    
    if len(sys.argv) != 2:
        print("使用方法: python fix_dify_url.py <您的部署URL>")
        print("示例: python fix_dify_url.py https://weather-api-xxxx.onrender.com")
        print("\n请提供您的Render部署URL")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 验证URL格式
    if not validate_url(url):
        sys.exit(1)
    
    # 测试OpenAPI端点
    if not test_openapi_endpoint(url):
        print("\n❌ OpenAPI端点测试失败")
        print("请检查:")
        print("1. 部署是否完成")
        print("2. URL是否正确")
        print("3. 服务是否正常运行")
        sys.exit(1)
    
    # 更新配置文件
    if not update_openapi_config(url):
        sys.exit(1)
    
    print("\n🎉 配置修复完成！")
    print("\n📋 在Dify中使用以下信息:")
    print(f"工具名称: 天气查询工具")
    print(f"API文档URL: {url}/openapi.json")
    print(f"认证类型: 无认证")
    
    print("\n🧪 测试参数:")
    print("city=北京")
    
    print("\n如果仍然出现'invalid schema'错误，请:")
    print("1. 确保URL完全正确")
    print("2. 等待几分钟让部署完全生效")
    print("3. 在浏览器中访问OpenAPI文档确认格式正确")

if __name__ == "__main__":
    main()
