# 天气API服务

一个基于Flask的天气查询API服务，集成OpenWeatherMap API，支持Dify平台。

## 功能特性

- 🌤️ 实时天气查询
- 🌍 支持全球城市
- 🔧 简单易用的REST API
- 🤖 完美支持Dify集成
- 🚀 一键部署到Render

## API端点

### 基础信息
- **GET** `/` - 服务状态
- **GET** `/openapi.json` - API文档
- **GET** `/weather?city={城市名}` - 天气查询

### 示例请求

```bash
# 查询北京天气
curl "http://localhost:8000/weather?city=Beijing"

# 返回示例
{
  "city": "Beijing",
  "temperature": 19.94,
  "feels_like": 19.16,
  "description": "晴",
  "humidity": 45
}
```

## 快速开始

### 本地运行

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
export WEATHER_API_KEY=your_api_key_here
```

3. 启动服务
```bash
python main.py
```

### 部署到Render

详细部署指南请参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 环境变量

| 变量名 | 描述 | 必需 |
|--------|------|------|
| `WEATHER_API_KEY` | OpenWeatherMap API密钥 | ✅ |
| `PORT` | 服务端口 | ❌ (默认: 8000) |
| `HOST` | 服务主机 | ❌ (默认: 0.0.0.0) |

## 技术栈

- **Python 3.12+**
- **Flask** - Web框架
- **Requests** - HTTP客户端
- **OpenWeatherMap API** - 天气数据源

## 许可证

MIT License