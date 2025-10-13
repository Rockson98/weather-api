# Render 部署说明

## 自动部署步骤

1. **访问 Render 平台**
   - 打开 https://render.com
   - 使用 GitHub 账户登录

2. **连接 GitHub 仓库**
   - 点击 "New +" -> "Web Service"
   - 选择 "Connect a repository"
   - 选择您的 GitHub 仓库

3. **配置部署设置**
   - Name: weather-api
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Plan: Free

4. **环境变量设置**
   - 在 Environment Variables 中添加:
     - PYTHON_VERSION: 3.9.18
     - PORT: 10000

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成

## 手动部署步骤

如果自动部署失败，可以手动部署:

1. **创建 Render 账户**
   ```bash
   # 访问 https://render.com 注册账户
   ```

2. **创建 Web Service**
   ```bash
   # 在 Render 控制台创建新的 Web Service
   ```

3. **配置服务**
   - 选择 GitHub 仓库
   - 设置构建和启动命令
   - 配置环境变量

4. **部署**
   - 点击部署按钮
   - 等待部署完成

## 获取部署地址

部署完成后，Render 会提供一个类似以下的地址:
- https://weather-api-xxx.onrender.com

## 测试部署

```bash
# 健康检查
curl https://your-app-name.onrender.com/health

# 天气查询测试
curl -X POST https://your-app-name.onrender.com/tool/tianqi/query \
     -H "Content-Type: application/json" \
     -d '{"city": "北京", "type": "current"}'
```

## 更新 Dify 配置

部署成功后，更新 Dify 配置:

```bash
export WEATHER_API_URL="https://your-app-name.onrender.com"
python dify/deploy_to_dify.py
```

## Render 免费额度

- 750 小时/月
- 512MB RAM
- 休眠机制 (15分钟无活动后休眠)
- 冷启动时间约 30-60 秒

## 注意事项

1. **休眠机制**: 免费版会在 15 分钟无活动后休眠
2. **冷启动**: 休眠后首次访问需要 30-60 秒启动时间
3. **内存限制**: 免费版只有 512MB RAM
4. **带宽限制**: 有带宽使用限制

## 故障排除

1. **部署失败**: 检查 requirements.txt 和 main.py
2. **启动失败**: 检查端口配置和环境变量
3. **API 超时**: 可能是冷启动，等待 30-60 秒后重试