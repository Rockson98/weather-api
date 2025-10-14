# 🚀 Render部署指南

## 📋 部署前准备

### 1. 获取OpenWeatherMap API密钥
1. 访问 [OpenWeatherMap](https://openweathermap.org/api)
2. 注册账户并登录
3. 在API Keys页面创建新的API密钥
4. 复制API密钥（格式类似：`811a271ed44e1d5599d8e0c773417557`）

### 2. 准备GitHub仓库
确保您的代码已推送到GitHub仓库的main分支。

## 🔧 Render部署步骤

### 方法一：使用render.yaml配置（推荐）

1. **登录Render**
   - 访问 [render.com](https://render.com)
   - 使用GitHub账户登录

2. **创建新服务**
   - 点击 "New +" 按钮
   - 选择 "Web Service"
   - 连接您的GitHub仓库

3. **配置服务**
   - **Name**: `weather-api` (或您喜欢的名称)
   - **Environment**: `Python 3`
   - **Region**: 选择离您最近的区域
   - **Branch**: `main`
   - **Root Directory**: 留空（使用根目录）
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **设置环境变量**
   - 在 "Environment Variables" 部分添加：
     ```
     WEATHER_API_KEY = your_openweather_api_key_here
     PORT = 8000
     HOST = 0.0.0.0
     ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待构建完成（通常需要2-5分钟）

### 方法二：手动配置

1. **创建新服务**
   - 选择 "Web Service"
   - 连接GitHub仓库

2. **基本配置**
   ```
   Name: weather-api
   Environment: Python 3
   Region: 选择合适区域
   Branch: main
   ```

3. **构建和启动命令**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   ```

4. **环境变量**
   ```
   WEATHER_API_KEY = your_api_key_here
   PORT = 8000
   HOST = 0.0.0.0
   ```

## ✅ 部署验证

### 1. 检查服务状态
- 在Render仪表板中查看服务状态
- 确保状态显示为 "Live"

### 2. 测试API端点
```bash
# 测试服务状态
curl https://your-app-name.onrender.com/

# 测试天气查询
curl "https://your-app-name.onrender.com/weather?city=北京"

# 测试OpenAPI文档
curl https://your-app-name.onrender.com/openapi.json
```

### 3. 预期响应
**服务状态** (`GET /`):
```json
{
  "message": "天气API服务正在运行"
}
```

**天气查询** (`GET /weather?city=北京`):
```json
{
  "city": "Beijing",
  "temperature": 15.5,
  "feels_like": 14.8,
  "description": "多云",
  "humidity": 65
}
```

## 🔧 常见问题解决

### 问题1：构建失败
**错误**: `ModuleNotFoundError: No module named 'flask'`

**解决方案**:
- 检查 `requirements.txt` 文件是否存在
- 确保所有依赖都列在文件中
- 检查Python版本兼容性

### 问题2：服务启动失败
**错误**: `Port 8000 already in use`

**解决方案**:
- 确保环境变量 `PORT` 设置为 `8000`
- 检查 `HOST` 设置为 `0.0.0.0`

### 问题3：API密钥错误
**错误**: `API密钥未配置`

**解决方案**:
- 检查环境变量 `WEATHER_API_KEY` 是否正确设置
- 确保API密钥有效且未过期

### 问题4：天气查询失败
**错误**: `401 Unauthorized`

**解决方案**:
- 验证OpenWeatherMap API密钥
- 检查API密钥是否有权限访问天气数据

## 📊 监控和维护

### 1. 查看日志
- 在Render仪表板中点击服务名称
- 查看 "Logs" 标签页
- 监控错误和性能信息

### 2. 性能监控
- 免费计划有使用限制
- 监控请求量和响应时间
- 考虑升级到付费计划以获得更好性能

### 3. 自动部署
- 默认启用自动部署
- 每次推送到main分支都会自动重新部署
- 可以在设置中禁用自动部署

## 🔄 更新部署

### 1. 代码更新
```bash
# 本地修改代码
git add .
git commit -m "更新天气API功能"
git push origin main
```

### 2. 手动重新部署
- 在Render仪表板中点击 "Manual Deploy"
- 选择要部署的分支
- 点击 "Deploy"

## 🌐 自定义域名（可选）

### 1. 添加自定义域名
- 在服务设置中找到 "Custom Domains"
- 添加您的域名
- 按照说明配置DNS记录

### 2. SSL证书
- Render自动提供SSL证书
- 支持HTTPS访问

## 📱 Dify集成

部署完成后，您可以在Dify中使用以下信息：

### API端点
```
https://your-app-name.onrender.com/weather
```

### OpenAPI文档
```
https://your-app-name.onrender.com/openapi.json
```

### 参数
- `city`: 城市名称（必需）
- 支持中文城市名：北京、上海、广州等

## 🎯 最佳实践

1. **安全性**
   - 不要在代码中硬编码API密钥
   - 使用环境变量管理敏感信息

2. **性能**
   - 考虑添加缓存机制
   - 监控API调用频率

3. **错误处理**
   - 实现完善的错误处理
   - 提供有意义的错误信息

4. **文档**
   - 保持API文档更新
   - 提供使用示例

## 📞 技术支持

如果遇到问题：
1. 检查Render服务日志
2. 验证环境变量配置
3. 测试API密钥有效性
4. 查看本文档的故障排除部分

---

**部署完成后，您的天气API就可以在Dify中使用了！** 🎉
