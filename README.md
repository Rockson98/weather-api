# 天气API服务

一个基于Flask的天气查询API服务，支持Dify平台集成，可部署到Render等云平台。

## 🌟 功能特性

- 🌤️ 实时天气查询
- 🌍 支持全球城市
- 🇨🇳 中文界面
- 🔧 易于集成Dify
- 📊 标准化API接口
- 🛡️ 错误处理机制
- ☁️ 云平台部署支持

## 🚀 快速开始

### 本地开发

1. **克隆仓库**
```bash
git clone https://github.com/your-username/weather-api.git
cd weather-api
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 创建.env文件
echo "WEATHER_API_KEY=your_openweather_api_key_here" > .env
```

4. **启动服务**
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

### 云平台部署

#### Render部署

1. **Fork本仓库到您的GitHub账户**

2. **在Render中创建新服务**
   - 选择 "Web Service"
   - 连接您的GitHub仓库
   - 配置环境变量

3. **环境变量配置**
```
WEATHER_API_KEY=your_openweather_api_key_here
```

4. **部署设置**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

## 📚 API文档

### 获取天气信息

**请求**:
```
GET /weather?city=北京
```

**响应**:
```json
{
  "city": "北京",
  "temperature": 15.5,
  "description": "多云",
  "humidity": 65
}
```

### API端点

- `GET /` - 服务状态
- `GET /weather` - 天气查询
- `GET /openapi.json` - OpenAPI文档

## 🔗 Dify集成

### 配置步骤

1. **部署API到Render**
2. **在Dify中创建自定义工具**
   - 工具类型: API工具
   - API端点: `https://your-app-name.onrender.com/weather`
   - 请求方法: GET
   - 参数: `city` (string, 必需)

3. **在应用中使用工具**

详细集成指南请参考 [DIFY_INTEGRATION_GUIDE.md](DIFY_INTEGRATION_GUIDE.md)

## 🛠️ 开发

### 项目结构

```
weather-api/
├── main.py                          # 主应用入口
├── tianqi_webtool/                  # 天气工具包
│   ├── server.py                   # Flask服务器
│   ├── client.py                   # 客户端
│   ├── config.py                   # 配置
│   └── schemas.py                   # 数据模型
├── dify_tool/                      # Dify工具文件
├── requirements.txt                # Python依赖
├── .gitignore                      # Git忽略文件
└── README.md                       # 项目说明
```

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `WEATHER_API_KEY` | OpenWeatherMap API密钥 | 必需 |
| `PORT` | 服务端口 | 8000 |
| `HOST` | 服务主机 | 0.0.0.0 |

## 🧪 测试

### 本地测试

```bash
# 测试服务状态
curl http://localhost:8000/

# 测试天气查询
curl "http://localhost:8000/weather?city=北京"
```

### 生产环境测试

```bash
# 替换为您的Render URL
curl https://your-app-name.onrender.com/weather?city=北京
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请创建Issue或联系维护者。
