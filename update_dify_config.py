#!/usr/bin/env python3
"""
Dify配置更新脚本
自动更新manifest.json和openapi.json中的API URL
"""

import json
import os
import sys

def update_config_files(deployment_url):
    """更新Dify配置文件中的URL"""
    
    # 移除末尾的斜杠
    if deployment_url.endswith('/'):
        deployment_url = deployment_url[:-1]
    
    print(f"正在更新配置文件，部署URL: {deployment_url}")
    
    # 更新 manifest.json
    manifest_path = "dify_tool/manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        manifest['api']['url'] = f"{deployment_url}/openapi.json"
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已更新 {manifest_path}")
    else:
        print(f"❌ 未找到 {manifest_path}")
    
    # 更新 openapi.json
    openapi_path = "dify_tool/openapi.json"
    if os.path.exists(openapi_path):
        with open(openapi_path, 'r', encoding='utf-8') as f:
            openapi = json.load(f)
        
        # 更新服务器URL
        openapi['servers'] = [
            {
                "url": deployment_url,
                "description": "Render生产服务器"
            }
        ]
        
        with open(openapi_path, 'w', encoding='utf-8') as f:
            json.dump(openapi, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已更新 {openapi_path}")
    else:
        print(f"❌ 未找到 {openapi_path}")

def main():
    if len(sys.argv) != 2:
        print("使用方法: python update_dify_config.py <部署URL>")
        print("示例: python update_dify_config.py https://weather-api-xxxx.onrender.com")
        sys.exit(1)
    
    deployment_url = sys.argv[1]
    update_config_files(deployment_url)
    
    print("\n🎉 配置文件更新完成！")
    print("\n下一步操作：")
    print("1. 提交更新的配置文件到Git")
    print("2. 在Dify中添加工具，使用以下URL：")
    print(f"   {deployment_url}/openapi.json")
    print("3. 测试工具功能")

if __name__ == "__main__":
    main()
