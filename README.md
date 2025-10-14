# 🌤️ 天气API服务 - Dify集成版

一个基于Flask的天气查询API服务，专为Dify平台设计，支持多支路工作流，可部署到Render等云平台。

## 🌟 功能特性

- 🌤️ 实时天气查询
- 🌍 支持全球城市
- 🇨🇳 中文界面
- 🔧 专为Dify优化
- 📊 标准化API接口
- 🛡️ 完善的错误处理
- ☁️ 云平台部署支持
- 🔄 多支路工作流支持

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

## 🔗 Dify集成

### 方案A：简单集成（推荐新手）

1. **部署API到Render**
2. **在Dify中创建自定义工具**
   - 工具类型: API工具
   - API端点: `https://your-app-name.onrender.com/weather`
   - 请求方法: GET
   - 参数: `city` (string, 必需)

3. **在应用中使用工具**

### 方案B：多支路工作流（推荐高级用户）

使用我们提供的多支路工作流方案，支持：
- 天气播报生成
- 散文创作
- 图片生成
- 数据合并

详细配置请参考：
- [Dify多支路工作流配置指南](dify_solution_b_setup_guide.md)
- [LLM节点配置指南](dify_solution_b_llm_config_guide.md)

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
  "humidity": 65,
  "wind_speed": 3.2,
  "pressure": 1013,
  "visibility": 10000,
  "feels_like": 14.8
}
```

### API端点

- `GET /` - 服务状态
- `GET /weather` - 天气查询
- `GET /openapi.json` - OpenAPI文档

## 🛠️ 项目结构

```
weather-api/
├── main.py                                    # 主应用入口
├── tianqi_webtool/                           # 天气工具包
│   ├── server.py                            # Flask服务器
│   ├── client.py                            # 客户端
│   ├── config.py                            # 配置
│   ├── schemas.py                           # 数据模型
│   └── openweather_client.py                # OpenWeather客户端
├── dify_tool/                               # Dify工具文件
│   ├── manifest.json                        # 工具清单
│   ├── openapi.json                         # API文档
│   └── weather_tool.py                      # 工具实现
├── dify_solution_b_*.py                     # Dify多支路工作流方案
├── requirements.txt                         # Python依赖
├── render.yaml                             # Render部署配置
└── README.md                               # 项目说明
```

## 🔧 环境变量

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

## 📖 详细文档

- [Dify集成完整指南](DIFY_INTEGRATION_GUIDE.md)
- [多支路工作流配置](dify_solution_b_setup_guide.md)
- [LLM节点配置指南](dify_solution_b_llm_config_guide.md)

## 🎯 使用示例

### 简单查询
用户询问："北京今天天气怎么样？"

Dify应用会：
1. 调用天气查询工具
2. 传入参数：`city=北京`
3. 获取天气数据
4. 返回友好格式的天气信息

### 多支路工作流
用户询问："给我写一篇关于北京天气的散文"

Dify应用会：
1. 获取天气数据
2. 生成天气播报
3. 创作天气散文
4. 合并输出结果

## ❓ 常见问题

**Q: API返回500错误？**
A: 检查OpenWeatherMap API密钥是否正确设置

**Q: Dify无法连接工具？**
A: 确认API服务已部署且openapi.json可访问

**Q: 天气数据不准确？**
A: 确认城市名称拼写正确，检查API响应

**Q: 多支路工作流不工作？**
A: 检查代码执行节点的参数配置和输出变量

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请创建Issue或联系维护者。