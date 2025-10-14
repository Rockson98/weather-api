#!/usr/bin/env python3
"""
Dify集成部署脚本
自动化完成从部署到集成的整个流程
"""

import os
import sys
import subprocess
import requests
import json
import time

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout:
                print(f"输出: {result.stdout}")
        else:
            print("❌ 失败")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False
    
    return True

def check_git_status():
    """检查Git状态"""
    print("\n📋 检查Git状态...")
    
    # 检查是否有未提交的更改
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("⚠️  发现未提交的更改:")
        print(result.stdout)
        return False
    else:
        print("✅ Git工作区干净")
        return True

def push_to_github():
    """推送到GitHub"""
    print("\n🚀 推送到GitHub...")
    
    # 添加所有文件
    if not run_command("git add .", "添加文件到暂存区"):
        return False
    
    # 提交更改
    if not run_command('git commit -m "准备部署到Render"', "提交更改"):
        return False
    
    # 推送到GitHub
    if not run_command("git push origin main", "推送到GitHub"):
        return False
    
    return True

def wait_for_deployment(url, max_attempts=30):
    """等待部署完成"""
    print(f"\n⏳ 等待部署完成: {url}")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{url}/", timeout=5)
            if response.status_code == 200:
                print("✅ 部署完成！")
                return True
        except:
            pass
        
        print(f"   尝试 {attempt + 1}/{max_attempts}...")
        time.sleep(10)
    
    print("❌ 部署超时")
    return False

def update_config_files(url):
    """更新配置文件"""
    print(f"\n🔧 更新配置文件...")
    
    # 更新 manifest.json
    manifest_path = "dify_tool/manifest.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        manifest['api']['url'] = f"{url}/openapi.json"
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        print("✅ 已更新 manifest.json")
    
    # 更新 openapi.json
    openapi_path = "dify_tool/openapi.json"
    if os.path.exists(openapi_path):
        with open(openapi_path, 'r', encoding='utf-8') as f:
            openapi = json.load(f)
        
        openapi['servers'] = [
            {
                "url": url,
                "description": "Render生产服务器"
            }
        ]
        
        with open(openapi_path, 'w', encoding='utf-8') as f:
            json.dump(openapi, f, ensure_ascii=False, indent=2)
        
        print("✅ 已更新 openapi.json")

def test_api(url):
    """测试API功能"""
    print(f"\n🧪 测试API功能...")
    
    try:
        # 测试OpenAPI文档
        response = requests.get(f"{url}/openapi.json", timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI文档可访问")
        else:
            print(f"❌ OpenAPI文档返回状态码: {response.status_code}")
            return False
        
        # 测试天气API
        response = requests.get(f"{url}/weather?city=北京", timeout=10)
        if response.status_code == 200:
            weather_data = response.json()
            print(f"✅ 天气API测试成功 - 北京: {weather_data.get('temperature')}°C")
        else:
            print(f"❌ 天气API返回状态码: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def main():
    print("🎯 Dify天气工具集成部署脚本")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) != 2:
        print("使用方法: python deploy_to_dify.py <部署URL>")
        print("示例: python deploy_to_dify.py https://weather-api-xxxx.onrender.com")
        print("\n注意: 请先在Render上创建部署，然后使用此脚本完成集成。")
        sys.exit(1)
    
    deployment_url = sys.argv[1]
    
    # 检查Git状态
    if not check_git_status():
        print("\n❌ 请先提交所有更改后再运行此脚本")
        sys.exit(1)
    
    # 推送到GitHub
    if not push_to_github():
        print("\n❌ 推送到GitHub失败")
        sys.exit(1)
    
    # 等待部署
    if not wait_for_deployment(deployment_url):
        print("\n❌ 部署失败或超时")
        sys.exit(1)
    
    # 更新配置文件
    update_config_files(deployment_url)
    
    # 测试API
    if not test_api(deployment_url):
        print("\n❌ API测试失败")
        sys.exit(1)
    
    # 显示集成信息
    print("\n🎉 部署和配置完成！")
    print("\n📋 下一步操作：")
    print("1. 在Dify中添加工具")
    print("2. 使用以下URL:")
    print(f"   {deployment_url}/openapi.json")
    print("3. 工具名称: 天气查询工具")
    print("4. 测试工具功能")
    
    print("\n📖 详细说明请查看: DIFY_INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()
