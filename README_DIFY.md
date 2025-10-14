# 🌤️ Dify天气工具集成

这是一个专为Dify平台设计的天气查询工具，可以获取指定城市的当前天气信息。

## 🚀 快速开始

### 1. 部署API服务

#### 方法一：使用自动化脚本（推荐）
```bash
# 1. 在Render上创建部署，获取部署URL
# 2. 运行自动化脚本
python deploy_to_dify.py https://your-app-name.onrender.com
```

#### 方法二：手动部署
```bash
# 1. 推送代码到GitHub
git add .
git commit -m "准备部署"
git push origin main

# 2. 在Render上创建Web Service
# 3. 设置环境变量：WEATHER_API_KEY
# 4. 等待部署完成
```

### 2. 在Dify中集成工具

1. **登录Dify** → 进入"工具"页面
2. **添加工具** → 选择"OpenAPI"
3. **配置信息**：
   - 工具名称：`天气查询工具`
   - API文档URL：`https://your-app-name.onrender.com/openapi.json`
   - 认证类型：`无认证`
4. **测试工具** → 输入`city=北京`
5. **保存并启用**

### 3. 在应用中使用

在Dify应用中添加工具节点，配置参数：
- **city**: 从用户输入获取城市名称

## 📁 项目结构

```
weather-api/
├── tianqi_webtool/          # 天气API核心代码
│   ├── server.py           # Flask服务器
│   ├── client.py           # 天气客户端
│   └── schemas.py          # 数据模型
├── dify_tool/              # Dify工具配置
│   ├── manifest.json       # 工具清单
│   └── openapi.json        # API文档
├── main.py                 # 应用入口
├── requirements.txt        # 依赖包
└── render.yaml            # Render部署配置
```

## 🔧 配置说明

### 环境变量
- `WEATHER_API_KEY`: OpenWeatherMap API密钥（必需）
- `PORT`: 服务端口（默认8000）
- `HOST`: 服务主机（默认0.0.0.0）

### API端点
- `GET /weather?city=城市名` - 获取天气信息
- `GET /openapi.json` - OpenAPI文档
- `GET /` - 健康检查

## 🧪 测试

### 测试API服务
```bash
# 检查部署状态
python check_deployment.py https://your-app-name.onrender.com

# 测试天气API
curl "https://your-app-name.onrender.com/weather?city=北京"
```

### 测试Dify集成
在Dify工具测试中输入：
- 参数：`city=北京`
- 预期返回：包含温度、天气描述、湿度等信息

## 📖 详细文档

- [完整集成指南](DIFY_INTEGRATION_GUIDE.md)
- [API文档](https://your-app-name.onrender.com/openapi.json)

## 🛠️ 工具脚本

- `deploy_to_dify.py` - 自动化部署脚本
- `check_deployment.py` - 部署状态检查
- `update_dify_config.py` - 配置文件更新

## ❓ 常见问题

**Q: API返回500错误？**
A: 检查OpenWeatherMap API密钥是否正确设置

**Q: Dify无法连接工具？**
A: 确认API服务已部署且openapi.json可访问

**Q: 天气数据不准确？**
A: 确认城市名称拼写正确，检查API响应

## 🎯 使用示例

用户询问："北京今天天气怎么样？"

Dify应用会：
1. 调用天气查询工具
2. 传入参数：`city=北京`
3. 获取天气数据
4. 返回友好格式的天气信息

## 📞 支持

如有问题，请检查：
1. Render部署日志
2. Dify工具测试结果
3. API端点响应
4. 配置文件正确性
