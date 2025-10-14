# 方案B：三条支路并行处理 - 完整配置指南

## 🏗️ 工作流架构

```
天气API → 主数据处理节点 → 分支器
                    ├── 支路1: 天气播报节点
                    ├── 支路2: 散文生成节点  
                    └── 支路3: 图片生成节点
```

## 🛠️ 详细配置步骤

### 步骤1: 创建主数据处理节点

1. **添加代码执行节点**
   - 节点名称：`主数据处理`
   - 输入参数：`weather_data` (天气API数据), `city` (城市名称)
   - 代码：复制 `dify_solution_b_main_processor.py` 中的代码

2. **配置输出参数**
   ```
   city, temperature, feels_like, weather_description, humidity, 
   pressure, wind_speed, visibility, weather_summary, weather_index,
   broadcast_data, prose_data, image_data
   ```

### 步骤2: 配置分支器

1. **添加分支器节点**
   - 节点名称：`数据分发器`
   - 输入：主数据处理节点的输出
   - 配置三个输出分支

2. **分支配置**
   - 分支1：天气播报数据 → 支路1
   - 分支2：散文生成数据 → 支路2
   - 分支3：图片生成数据 → 支路3

### 步骤3: 配置支路1 - 天气播报节点

1. **添加代码执行节点**
   - 节点名称：`天气播报`
   - 输入参数：`city, temperature, feels_like, weather_description, humidity, pressure, wind_speed, visibility`
   - 代码：复制 `dify_solution_b_branch1_weather.py` 中的代码

2. **输出参数**
   ```
   weather_broadcast, short_summary, detailed_report, 
   weather_icon, temperature_feeling, humidity_description, 
   wind_description, visibility_description, weather_tips
   ```

### 步骤4: 配置支路2 - 散文生成节点

1. **添加代码执行节点**
   - 节点名称：`散文生成`
   - 输入参数：`city, temperature, feels_like, weather_description, humidity, pressure, wind_speed, visibility`
   - 代码：复制 `dify_solution_b_branch2_prose.py` 中的代码

2. **输出参数**
   ```
   prose_prompt, prose_context, prose_instruction, prose_style,
   keywords, season, time_description, city_characteristics,
   weather_mood, writing_tone
   ```

3. **添加LLM节点（可选）**
   - 节点名称：`散文LLM`
   - 输入：`prose_prompt` 和 `prose_context`
   - 模型：选择您喜欢的LLM模型

### 步骤5: 配置支路3 - 图片生成节点

1. **添加代码执行节点**
   - 节点名称：`图片生成`
   - 输入参数：`city, temperature, feels_like, weather_description, humidity, pressure, wind_speed, visibility`
   - 代码：复制 `dify_solution_b_branch3_image.py` 中的代码

2. **输出参数**
   ```
   image_prompt_en, image_prompt_cn, image_description, image_style,
   image_quality, image_size, keywords, season, time_description,
   city_characteristics, weather_mood, visual_elements
   ```

3. **添加图像生成节点（可选）**
   - 节点名称：`图像生成`
   - 输入：`image_prompt_en` 和 `image_description`
   - 模型：选择图像生成模型

## 🔧 节点连接配置

### 连接顺序
1. `天气API` → `主数据处理`
2. `主数据处理` → `数据分发器`
3. `数据分发器` → `天气播报`
4. `数据分发器` → `散文生成`
5. `数据分发器` → `图片生成`

### 数据流配置
- **天气API** 输出 → **主数据处理** 输入
- **主数据处理** 输出 → **数据分发器** 输入
- **数据分发器** 输出 → 三个支路节点

## 🧪 测试步骤

### 1. 单元测试
- 测试主数据处理节点
- 测试每个支路节点
- 验证数据格式和内容

### 2. 集成测试
- 测试完整工作流
- 验证三个支路都能正常输出
- 检查数据传递是否正确

### 3. 性能测试
- 测试并行处理效率
- 检查资源使用情况
- 优化响应时间

## 🎨 预期输出效果

### 支路1: 天气播报
```
🌤️ 北京天气播报
📅 2024年01月15日 14:30 Monday

⛅ 天气状况：多云
🌡️ 温度：15°C (舒适)
🤔 体感温度：12°C
💧 湿度：65% (适宜)
📊 气压：1013 hPa
💨 风速：3 m/s (轻风)
👁️ 能见度：10 km (良好)

💡 温馨提示：
天气适宜，祝您愉快！
```

### 支路2: 散文生成
```
【散文提示词】
请为北京这座城市写一段优美的散文，描述当前的天气状况。

【城市背景】
古都北京，有着深厚的历史文化底蕴，胡同巷陌间藏着老北京的味道

【天气信息】
- 城市：北京
- 时间：下午
- 季节：春秋
- 温度：15°C
- 体感温度：12°C
- 天气状况：多云
...
```

### 支路3: 图片生成
```
【英文提示词】
A beautiful weather scene in 北京 city, 多云, 
temperature 15°C, feels like 12°C, 
humidity 65%, atmospheric pressure 1013hPa, 
wind speed 3m/s, visibility 10km, 
spring season, afternoon time, 
realistic photography style, high quality, detailed, 
urban landscape, weather atmosphere, natural lighting, 
cloudy sky, soft diffused light, dramatic cloud formations
```

## 🔍 故障排除

### 常见问题
1. **数据传递错误**
   - 检查分支器的输入输出配置
   - 确保数据正确分发到各支路

2. **支路节点错误**
   - 检查各支路节点的输入参数
   - 确保数据格式正确

3. **代码执行错误**
   - 检查代码语法
   - 确保所有函数都正确定义

### 调试技巧
1. **逐步测试** - 从单个节点开始测试
2. **日志记录** - 添加日志记录便于调试
3. **数据检查** - 检查每个节点的输入输出数据

## 🚀 优化建议

### 性能优化
1. **并行处理** - 利用三个支路的并行性
2. **缓存机制** - 缓存重复的API调用
3. **资源管理** - 合理分配计算资源

### 功能扩展
1. **多语言支持** - 添加多语言天气播报
2. **个性化定制** - 根据用户偏好调整输出
3. **历史记录** - 保存历史天气数据

## 📊 监控和维护

### 监控指标
1. **成功率** - 各支路的成功执行率
2. **响应时间** - 各节点的处理时间
3. **错误率** - 各节点的错误发生率

### 维护建议
1. **定期检查** - 定期检查工作流状态
2. **日志分析** - 分析日志找出问题
3. **性能优化** - 根据监控数据优化性能
