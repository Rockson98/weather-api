# Dify 天气工具集成指南

## 📋 概述

本指南将帮助您将天气API工具集成到Dify平台中。您的天气工具已经配置好了所有必要的文件，现在需要完成部署和集成步骤。

## 🚀 步骤1：部署API服务

### 1.1 推送代码到GitHub
```bash
# 确保所有文件都已提交
git add .
git commit -m "准备部署到Render"
git push origin main
```

### 1.2 在Render上部署
1. 访问 [Render Dashboard](https://dashboard.render.com/)
2. 点击 "New +" → "Web Service"
3. 连接您的GitHub仓库
4. 配置部署设置：
   - **Name**: `weather-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

### 1.3 设置环境变量
在Render Dashboard中设置以下环境变量：
- `WEATHER_API_KEY`: 您的OpenWeatherMap API密钥
- `PORT`: `8000`
- `HOST`: `0.0.0.0`

### 1.4 获取部署URL
部署完成后，您会得到一个类似这样的URL：
```
https://weather-api-xxxx.onrender.com
```

## 🔧 步骤2：更新配置文件

### 2.1 更新manifest.json
将 `dify_tool/manifest.json` 中的URL更新为您的实际部署URL：

```json
{
  "schema_version": "v1",
  "name_for_human": "天气查询工具",
  "name_for_model": "weather_tool",
  "description_for_human": "获取指定城市的当前天气信息和天气预报",
  "description_for_model": "一个用于查询天气信息的工具，可以获取当前天气、天气预报等数据。支持中文城市名称查询。",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://your-actual-app-name.onrender.com/openapi.json"
  },
  "logo_url": "https://cdn-icons-png.flaticon.com/512/1163/1163661.png",
  "contact_email": "your-email@example.com",
  "legal_info_url": "https://example.com/legal"
}
```

### 2.2 更新openapi.json
将 `dify_tool/openapi.json` 中的服务器URL更新：

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "天气API服务",
    "description": "提供天气查询功能的API服务",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-actual-app-name.onrender.com",
      "description": "Render生产服务器"
    }
  ],
  // ... 其余配置保持不变
}
```

## 🎯 步骤3：在Dify中集成工具

### 3.1 访问Dify工具管理
1. 登录您的Dify账户
2. 进入 "工具" 或 "Tools" 页面
3. 点击 "添加工具" 或 "Add Tool"

### 3.2 选择工具类型
选择 "OpenAPI" 或 "API工具" 类型

### 3.3 配置工具信息
填写以下信息：

**基本信息：**
- **工具名称**: `天气查询工具`
- **工具描述**: `获取指定城市的当前天气信息和天气预报`
- **API文档URL**: `https://your-actual-app-name.onrender.com/openapi.json`

**认证设置：**
- **认证类型**: `无认证` 或 `None`

### 3.4 测试工具
1. 点击 "测试" 按钮
2. 输入测试参数：`city=北京`
3. 确认返回正确的天气数据

### 3.5 保存并启用
1. 测试通过后，点击 "保存"
2. 确保工具状态为 "已启用"

## 🔄 步骤4：在应用中使用工具

### 4.1 创建或编辑应用
1. 进入 "应用" 页面
2. 创建新应用或编辑现有应用

### 4.2 添加工具到工作流
1. 在应用编辑器中，添加 "工具" 节点
2. 选择您刚创建的 "天气查询工具"
3. 配置工具参数：
   - **city**: 从用户输入或变量中获取城市名称

### 4.3 配置提示词
在系统提示词中添加工具使用说明：

```
你是一个天气助手，可以帮助用户查询天气信息。

当用户询问天气时，请使用天气查询工具获取准确的天气数据。

工具使用方法：
- 调用天气查询工具，传入城市名称
- 将获取到的天气信息以友好的方式展示给用户

示例：
用户：北京今天天气怎么样？
助手：我来为您查询北京的天气信息。
[调用天气查询工具，city=北京]
根据最新数据，北京今天天气晴朗，温度25°C，湿度60%。
```

## 🧪 步骤5：测试集成

### 5.1 测试API端点
在浏览器中访问：
```
https://your-actual-app-name.onrender.com/weather?city=北京
```

应该返回类似这样的JSON数据：
```json
{
  "city": "北京",
  "temperature": 25.0,
  "description": "晴朗",
  "humidity": 60
}
```

### 5.2 测试Dify应用
1. 在Dify中发布您的应用
2. 在聊天界面测试：
   - "北京天气怎么样？"
   - "上海今天温度多少？"
   - "深圳的天气情况"

## 🔍 故障排除

### 常见问题及解决方案

**1. API返回500错误**
- 检查OpenWeatherMap API密钥是否正确设置
- 确认API密钥有足够的调用次数

**2. Dify无法连接工具**
- 确认API服务已成功部署
- 检查openapi.json中的URL是否正确
- 确认CORS设置允许Dify访问

**3. 工具测试失败**
- 检查网络连接
- 确认API端点可正常访问
- 查看Render日志排查问题

**4. 天气数据不准确**
- 确认城市名称拼写正确
- 检查OpenWeatherMap API的响应数据

## 📞 技术支持

如果遇到问题，可以：
1. 查看Render部署日志
2. 检查Dify工具测试结果
3. 验证API端点响应
4. 确认所有配置文件正确

## 🎉 完成！

恭喜！您已经成功将天气API工具集成到Dify中。现在您可以在Dify应用中为用户提供准确的天气查询服务了。
