# 🚀 部署指南

## ✅ 本地测试完成

您的天气API已经在本地成功运行！测试结果显示：
- ✅ API密钥配置正确
- ✅ 服务器正常启动
- ✅ 天气查询功能正常
- ✅ 返回正确的JSON数据

## 🌐 部署到Render

### 第一步：推送代码到GitHub

```bash
git add .
git commit -m "配置API密钥并测试通过"
git push origin main
```

### 第二步：在Render中部署

1. **登录Render**
   - 访问 [render.com](https://render.com)
   - 使用您的GitHub账户登录

2. **创建新的Web服务**
   - 点击 "New" -> "Web Service"
   - 连接您的GitHub仓库
   - 选择 `weather-api` 仓库

3. **配置服务设置**
   - **Name**: `weather-api` (或您喜欢的名称)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **设置环境变量**
   在 "Environment Variables" 部分添加：
   ```
   WEATHER_API_KEY = 811a271ed44e1d5599d8e0c773417557
   PORT = 8000
   HOST = 0.0.0.0
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成（通常需要2-5分钟）

### 第三步：测试部署的API

部署完成后，您会得到一个URL，例如：
`https://your-app-name.onrender.com`

测试API：
```bash
curl "https://your-app-name.onrender.com/"
curl "https://your-app-name.onrender.com/weather?city=Beijing"
```

## 🔧 Dify集成

### 配置Dify工具

1. **在Dify中创建工具**
   - 进入您的Dify应用
   - 选择 "工具" -> "天气API"

2. **设置API端点**
   - **API URL**: `https://your-app-name.onrender.com`
   - **端点**: `/weather`
   - **参数**: `city` (城市名称)

3. **测试集成**
   - 在Dify的调试页面测试天气查询
   - 确保能够成功获取天气信息

## 📋 部署检查清单

- [ ] 代码已推送到GitHub
- [ ] Render服务已创建
- [ ] 环境变量已配置
- [ ] 部署成功完成
- [ ] API端点测试通过
- [ ] Dify集成配置完成
- [ ] 端到端测试通过

## 🆘 故障排除

### 常见问题

1. **部署失败**
   - 检查 `requirements.txt` 文件是否存在
   - 确认Python版本兼容性

2. **API返回错误**
   - 验证环境变量是否正确设置
   - 检查API密钥是否有效

3. **Dify集成失败**
   - 确认Render服务URL正确
   - 检查网络连接和CORS设置

### 获取帮助

如果遇到问题，请检查：
- Render部署日志
- API响应状态码
- 环境变量配置

## 🎉 完成

部署完成后，您的天气API将：
- ✅ 在Render上稳定运行
- ✅ 支持全球访问
- ✅ 与Dify完美集成
- ✅ 提供实时天气数据

祝您使用愉快！
