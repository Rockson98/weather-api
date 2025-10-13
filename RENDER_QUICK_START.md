# 🚀 Render 免费托管快速部署指南

## 📋 部署前准备

✅ **已完成**：
- Git仓库已初始化
- 所有文件已提交
- Render配置文件已创建

## 🎯 下一步：部署到Render

### 第一步：创建GitHub仓库

1. **访问GitHub**
   - 打开 https://github.com
   - 登录您的账户

2. **创建新仓库**
   - 点击 "New repository"
   - 仓库名称：`weather-api` (或您喜欢的名称)
   - 设置为 Public (免费版Render需要)
   - 不要初始化README (我们已经有了)

3. **推送代码到GitHub**
   ```bash
   # 添加远程仓库 (替换yourusername为您的GitHub用户名)
   git remote add origin https://github.com/yourusername/weather-api.git
   
   # 推送到GitHub
   git push -u origin master
   ```

### 第二步：在Render上部署

1. **访问Render平台**
   - 打开 https://render.com
   - 使用GitHub账户登录

2. **创建Web Service**
   - 点击 "New +" → "Web Service"
   - 选择 "Connect a repository"
   - 选择您刚创建的GitHub仓库

3. **配置部署设置**
   ```
   Name: weather-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Plan: Free
   ```

4. **环境变量设置**
   在Environment Variables中添加：
   ```
   PYTHON_VERSION: 3.9.18
   PORT: 10000
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成（通常需要2-5分钟）

### 第三步：测试部署

部署完成后，您会得到一个类似这样的地址：
```
https://weather-api-xxx.onrender.com
```

**测试命令**：
```bash
# 健康检查
curl https://your-app-name.onrender.com/health

# 天气查询测试
curl -X POST https://your-app-name.onrender.com/tool/tianqi/query \
     -H "Content-Type: application/json" \
     -d '{"city": "北京", "type": "current"}'
```

### 第四步：配置Dify集成

部署成功后，更新Dify配置：
```bash
export WEATHER_API_URL="https://your-app-name.onrender.com"
python dify/deploy_to_dify.py
```

## 📊 Render免费额度

| 项目 | 免费额度 |
|------|----------|
| 运行时间 | 750小时/月 |
| 内存 | 512MB RAM |
| 休眠机制 | 15分钟无活动后休眠 |
| 冷启动时间 | 30-60秒 |
| 带宽 | 有限制 |

## ⚠️ 重要注意事项

1. **休眠机制**：免费版会在15分钟无活动后自动休眠
2. **冷启动**：休眠后首次访问需要30-60秒启动时间
3. **内存限制**：只有512MB RAM，适合轻量级应用
4. **带宽限制**：有带宽使用限制

## 🔧 故障排除

### 常见问题

1. **部署失败**
   - 检查 `requirements.txt` 文件
   - 确保 `main.py` 文件存在且正确

2. **启动失败**
   - 检查端口配置
   - 确保环境变量设置正确

3. **API超时**
   - 可能是冷启动，等待30-60秒后重试
   - 考虑使用付费版避免休眠

### 检查部署状态

在Render控制台查看：
- Build Logs：构建日志
- Runtime Logs：运行日志
- Metrics：性能指标

## 🎯 推荐使用场景

**适合Render免费版**：
- ✅ 个人项目或演示
- ✅ 低频率访问的应用
- ✅ 开发测试环境
- ✅ 预算有限的项目

**不适合的情况**：
- ❌ 高频率访问的生产环境
- ❌ 需要快速响应的应用
- ❌ 商业项目

## 📈 升级建议

如果免费版不够用，可以考虑：

1. **Render付费版**：$7/月起，无休眠限制
2. **Railway**：$5/月免费额度
3. **云服务器**：阿里云/腾讯云等，更稳定

## 🆘 需要帮助？

如果遇到问题，可以：
1. 查看Render控制台的日志
2. 检查GitHub仓库是否正确推送
3. 确认环境变量设置
4. 测试本地API是否正常工作

---

**下一步**：按照上述步骤创建GitHub仓库并部署到Render！
