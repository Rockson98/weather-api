#!/usr/bin/env python3
"""
快速修复Dify集成问题
解决"invalid schema"错误
"""

import json
import requests
import sys

def get_render_url():
    """获取Render部署URL"""
    print("🔍 请提供您的Render部署URL")
    print("格式示例: https://weather-api-xxxx.onrender.com")
    print("您可以在Render Dashboard中找到这个URL")
    
    while True:
        url = input("\n请输入您的Render URL: ").strip()
        
        if not url:
            print("❌ URL不能为空，请重新输入")
            continue
            
        if not url.startswith(('http://', 'https://')):
            print("❌ URL必须以 http:// 或 https:// 开头")
            continue
            
        if not url.endswith('.onrender.com'):
            print("⚠️  警告: URL似乎不是Render部署地址")
            confirm = input("是否继续？(y/n): ").strip().lower()
            if confirm != 'y':
                continue
        
        # 移除末尾斜杠
        if url.endswith('/'):
            url = url[:-1]
            
        return url

def test_url(url):
    """测试URL是否可访问"""
    print(f"\n🧪 测试URL: {url}")
    
    try:
        # 测试根路径
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ 服务根路径可访问")
        else:
            print(f"⚠️  服务根路径返回状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法访问服务根路径: {e}")
        return False
    
    try:
        # 测试OpenAPI文档
        openapi_url = f"{url}/openapi.json"
        response = requests.get(openapi_url, timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI文档可访问")
            
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
            print(f"❌ OpenAPI文档返回状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法访问OpenAPI文档: {e}")
        return False

def update_openapi_config(url):
    """更新OpenAPI配置文件"""
    print(f"\n🔧 更新OpenAPI配置...")
    
    try:
        with open('dify_tool/openapi.json', 'r', encoding='utf-8') as f:
            openapi = json.load(f)
        
        # 更新服务器URL
        openapi['servers'] = [
            {
                "url": url,
                "description": "Render生产服务器"
            },
            {
                "url": "http://localhost:8000",
                "description": "本地开发服务器"
            }
        ]
        
        with open('dify_tool/openapi.json', 'w', encoding='utf-8') as f:
            json.dump(openapi, f, ensure_ascii=False, indent=2)
        
        print("✅ 已更新 dify_tool/openapi.json")
        return True
    except Exception as e:
        print(f"❌ 更新配置文件失败: {e}")
        return False

def main():
    print("🚀 Dify集成快速修复工具")
    print("=" * 40)
    
    # 获取Render URL
    url = get_render_url()
    
    # 测试URL
    if not test_url(url):
        print("\n❌ URL测试失败，请检查:")
        print("1. URL是否正确")
        print("2. 服务是否正在运行")
        print("3. 网络连接是否正常")
        return
    
    # 更新配置
    if not update_openapi_config(url):
        print("\n❌ 配置更新失败")
        return
    
    print("\n🎉 修复完成！")
    print("\n📋 在Dify中使用以下配置:")
    print(f"工具名称: 天气查询工具")
    print(f"API文档URL: {url}/openapi.json")
    print(f"认证类型: 无认证")
    
    print("\n🧪 测试参数:")
    print("city=北京")
    
    print("\n💡 如果仍然出现'invalid schema'错误:")
    print("1. 等待几分钟让配置生效")
    print("2. 清除浏览器缓存")
    print("3. 尝试使用不同的浏览器")

if __name__ == "__main__":
    main()
