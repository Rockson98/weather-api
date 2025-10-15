# 🔧 API配置指南

## 📋 问题诊断

根据测试结果，您遇到的404错误主要是由于 **API密钥未配置** 导致的。

## 🛠️ 解决步骤

### 第一步：获取OpenWeatherMap API密钥

1. **注册账户**
   - 访问 [OpenWeatherMap](https://openweathermap.org/api)
   - 注册免费账户

2. **获取API密钥**
   - 登录后进入 "API Keys" 页面
   - 复制您的API密钥（格式类似：`811a271ed44e1d5599d8e0c773417557`）

### 第二步：配置本地环境

1. **创建.env文件**
   在项目根目录创建 `.env` 文件：
   ```
   WEATHER_API_KEY=your_actual_api_key_here
   PORT=8000
   HOST=0.0.0.0
   ```

2. **测试本地API**
   ```bash
   python test_weather_api.py
   ```

### 第三步：部署到Render

1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "添加API密钥配置"
   git push origin main
   ```

2. **在Render中设置环境变量**
   - 登录 [render.com](https://render.com)
   - 进入您的服务设置
   - 在 "Environment Variables" 部分添加：
     ```
     WEATHER_API_KEY = your_actual_api_key_here
     PORT = 8000
     HOST = 0.0.0.0
     ```

3. **重新部署**
   - 点击 "Manual Deploy"
   - 等待部署完成

### 第四步：在Dify中配置

1. **获取正确的API URL**
   - 从Render控制台复制您的服务URL
   - 格式类似：`https://your-app-name.onrender.com`

2. **在Dify中配置工具**
   - API端点：`https://your-app-name.onrender.com/weather`
   - 请求方法：GET
   - 参数：`city` (string, 必需)

## 🔍 故障排除

### 问题1：API密钥未配置
**错误信息**：`{"error":"API密钥未配置"}`

**解决方案**：
- 检查.env文件是否存在
- 确认API密钥格式正确
- 重启服务器

### 问题2：404 Not Found
**可能原因**：
- API URL不正确
- 服务未正确部署
- 路由配置错误

**解决方案**：
- 验证Render服务状态
- 检查API端点URL
- 查看服务日志

### 问题3：城市查询失败
**可能原因**：
- 城市名称不支持
- API密钥权限不足

**解决方案**：
- 使用支持的城市名称（北京、上海、广州等）
- 检查API密钥是否有效

## 📊 测试验证

### 本地测试
```bash
# 启动服务器
python main.py

# 测试API
python test_weather_api.py
```

### 远程测试
```bash
# 测试服务状态
curl https://your-app-name.onrender.com/

# 测试天气查询
curl "https://your-app-name.onrender.com/weather?city=北京"
```

## 🎯 预期结果

### 成功的响应示例
```json
{
  "city": "Beijing",
  "temperature": 15.5,
  "feels_like": 14.8,
  "description": "多云",
  "humidity": 65
}
```

### 支持的城市
- 北京 (Beijing)
- 上海 (Shanghai)
- 广州 (Guangzhou)
- 深圳 (Shenzhen)
- 杭州 (Hangzhou)
- 南京 (Nanjing)
- 成都 (Chengdu)
- 武汉 (Wuhan)
- 西安 (Xian)
- 重庆 (Chongqing)

## 📞 技术支持

如果仍然遇到问题：
1. 检查Render服务日志
2. 验证API密钥有效性
3. 确认网络连接正常
4. 查看本文档的故障排除部分
