#!/usr/bin/env python3
"""
自动检测Render部署URL
基于GitHub仓库信息推测可能的URL
"""

import requests
import json
import subprocess
import sys

def get_github_repo():
    """获取GitHub仓库信息"""
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        url = result.stdout.strip()
        if 'github.com' in url:
            # 提取仓库名
            repo_name = url.split('/')[-1].replace('.git', '')
            return repo_name
    except:
        pass
    return None

def try_common_render_urls(repo_name):
    """尝试常见的Render URL格式"""
    possible_urls = [
        f"https://{repo_name}.onrender.com",
        f"https://{repo_name}-api.onrender.com",
        f"https://{repo_name}-service.onrender.com",
        f"https://weather-api.onrender.com",  # 基于项目名称
    ]
    
    print(f"🔍 尝试检测可能的Render URL...")
    
    for url in possible_urls:
        print(f"   测试: {url}")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ 找到可用的URL: {url}")
                return url
        except:
            continue
    
    return None

def test_openapi_endpoint(url):
    """测试OpenAPI端点"""
    try:
        openapi_url = f"{url}/openapi.json"
        response = requests.get(openapi_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'openapi' in data and 'paths' in data:
                return True
    except:
        pass
    return False

def main():
    print("🔍 自动检测Render部署URL")
    print("=" * 40)
    
    # 获取仓库名
    repo_name = get_github_repo()
    if repo_name:
        print(f"📦 检测到仓库: {repo_name}")
    else:
        print("⚠️  无法检测到GitHub仓库信息")
        repo_name = "weather-api"  # 使用默认名称
    
    # 尝试检测URL
    detected_url = try_common_render_urls(repo_name)
    
    if detected_url:
        print(f"\n🎉 检测到可用的Render URL: {detected_url}")
        
        # 测试OpenAPI端点
        if test_openapi_endpoint(detected_url):
            print("✅ OpenAPI端点测试通过")
            
            # 更新配置
            try:
                with open('dify_tool/openapi.json', 'r', encoding='utf-8') as f:
                    openapi = json.load(f)
                
                openapi['servers'] = [
                    {
                        "url": detected_url,
                        "description": "Render生产服务器"
                    },
                    {
                        "url": "http://localhost:8000",
                        "description": "本地开发服务器"
                    }
                ]
                
                with open('dify_tool/openapi.json', 'w', encoding='utf-8') as f:
                    json.dump(openapi, f, ensure_ascii=False, indent=2)
                
                print("✅ 已自动更新配置文件")
                
                print(f"\n📋 在Dify中使用以下配置:")
                print(f"工具名称: 天气查询工具")
                print(f"API文档URL: {detected_url}/openapi.json")
                print(f"认证类型: 无认证")
                
            except Exception as e:
                print(f"❌ 更新配置文件失败: {e}")
        else:
            print("❌ OpenAPI端点测试失败")
    else:
        print("\n❌ 无法自动检测到Render URL")
        print("\n请手动运行: python quick_fix_dify.py")
        print("然后提供您的实际Render部署URL")

if __name__ == "__main__":
    main()
