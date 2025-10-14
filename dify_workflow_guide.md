# Dify工作流：天气API + 内容生成完整指南

## 🎯 工作流目标
1. 通过天气API获取信息
2. 通过LLM基于天气信息和城市生成散文描述与图片描述
3. 通过图片生成工具生成对应图片
4. 整合所有信息输出

## 📋 代码执行节点配置

### 在代码执行节点的arg1中可以使用的变量：

#### 1. 天气API返回的原始数据
```python
# 天气API节点返回的完整响应
weather_response = arg1  # 这是天气API的完整响应对象

# 可访问的具体字段：
city = weather_response.get('city')           # 城市名称
temperature = weather_response.get('temperature')  # 温度（摄氏度）
description = weather_response.get('description')  # 天气描述
humidity = weather_response.get('humidity')    # 湿度（百分比）
```

#### 2. 工作流上下文变量
```python
# 从开始步骤传入的城市名称
input_city = arg2  # 这是用户输入的城市名称

# 其他可能的上下文变量（如果存在）
# workflow_id = context.get('workflow_id')
# user_id = context.get('user_id')
# session_id = context.get('session_id')
```

## 🔧 推荐的代码执行节点代码

```python
def main(arg1, arg2):
    """
    arg1: 天气API返回的数据（可能是列表或对象）
    arg2: 开始步骤输入的城市名称
    """
    
    # 1. 处理天气数据 - 确保是对象格式
    weather_data = arg1
    
    # 如果arg1是列表，取第一个元素
    if isinstance(weather_data, list) and len(weather_data) > 0:
        weather_data = weather_data[0]
    
    # 确保weather_data是字典
    if not isinstance(weather_data, dict):
        weather_data = {}
    
    # 提取天气信息
    city = weather_data.get('city', arg2)  # 优先使用API返回的城市名
    temperature = weather_data.get('temperature', 0)
    feels_like = weather_data.get('feels_like', 0)
    weather_desc = weather_data.get('description', '')
    humidity = weather_data.get('humidity', 0)
    
    # 2. 构建用于LLM的天气信息摘要
    weather_summary = {
        "城市": city,
        "温度": f"{temperature}°C",
        "体感温度": f"{feels_like}°C",
        "天气状况": weather_desc,
        "湿度": f"{humidity}%"
    }
    
    # 3. 构建图片描述提示词
    image_prompt = f"城市{city}的天气景象，{weather_desc}，温度{temperature}度，体感{feels_like}度，{humidity}%湿度，{get_weather_mood(weather_desc, temperature)}"
    
    # 4. 构建散文描述提示词
    prose_prompt = f"请为{city}这座城市写一段优美的散文，描述当前的天气状况：{weather_desc}，温度{temperature}度，体感温度{feels_like}度，湿度{humidity}%"
    
    # 5. 返回结构化数据供后续节点使用
    return {
        "weather_info": weather_summary,
        "image_prompt": image_prompt,
        "prose_prompt": prose_prompt,
        "city": city,
        "temperature": temperature,
        "feels_like": feels_like,
        "weather_description": weather_desc,
        "humidity": humidity,
        "raw_weather_data": weather_data
    }

def get_weather_mood(weather_desc, temperature):
    """根据天气状况生成情绪描述"""
    mood_map = {
        "晴": "阳光明媚，天空湛蓝",
        "多云": "云层密布，天空灰蒙",
        "雨": "细雨绵绵，空气清新",
        "雪": "雪花纷飞，银装素裹",
        "雾": "雾气朦胧，若隐若现",
        "阴": "阴云密布，略显沉闷"
    }
    
    for key, mood in mood_map.items():
        if key in weather_desc:
            return mood
    
    # 根据温度判断
    if temperature > 30:
        return "炎热干燥，阳光强烈"
    elif temperature > 20:
        return "温暖宜人，气候舒适"
    elif temperature > 10:
        return "凉爽清新，秋意盎然"
    else:
        return "寒冷刺骨，冬意浓浓"
```

## 🎨 工作流节点配置建议

### 1. 开始节点
- **输入变量**: `city` (城市名称)

### 2. 天气API节点
- **工具**: 天气查询工具
- **参数**: `city={{#start.city#}}`

### 3. 代码执行节点
- **arg1**: `{{#weather_api.weather#}}` (天气API返回数据)
- **arg2**: `{{#start.city#}}` (开始步骤的城市名称)

### 4. LLM节点1 - 散文生成
- **提示词**: `{{#code_execution.prose_prompt#}}`
- **输入变量**: 
  - `weather_info`: `{{#code_execution.weather_info#}}`

### 5. LLM节点2 - 图片描述优化
- **提示词**: `请优化以下图片描述，使其更适合AI绘画：{{#code_execution.image_prompt#}}`

### 6. 图片生成节点
- **提示词**: `{{#llm2.output#}}`
- **其他参数**: 根据您的图片生成工具配置

### 7. 最终整合节点
- **模板**: 
```
# {{#code_execution.city#}} 天气散文

## 天气信息
- 城市：{{#code_execution.city#}}
- 温度：{{#code_execution.temperature#}}°C
- 天气：{{#code_execution.weather_description#}}
- 湿度：{{#code_execution.humidity#}}%

## 散文描述
{{#llm1.output#}}

## 配图
{{#image_generation.output#}}
```

## 🔍 调试技巧

### 1. 在代码执行节点中添加调试输出
```python
def main(arg1, arg2):
    print(f"天气API数据: {arg1}")
    print(f"输入城市: {arg2}")
    
    # ... 您的处理逻辑 ...
    
    return result
```

### 2. 验证数据格式
```python
def main(arg1, arg2):
    # 检查arg1的数据结构
    if isinstance(arg1, dict):
        print("arg1是字典格式")
        print(f"可用键: {list(arg1.keys())}")
    else:
        print(f"arg1类型: {type(arg1)}")
        print(f"arg1内容: {arg1}")
    
    return {"debug": "检查控制台输出"}
```

## ⚠️ 注意事项

1. **变量引用格式**: 在Dify中使用 `{{#节点名.输出字段#}}` 格式
2. **数据类型**: 确保代码执行节点返回的数据类型与后续节点期望的匹配
3. **错误处理**: 在代码中添加适当的错误处理
4. **测试**: 建议先用简单数据测试工作流

## 🚀 快速测试

1. 将上述代码复制到代码执行节点
2. 运行工作流，输入城市名称（如"北京"）
3. 检查代码执行节点的输出是否符合预期
4. 根据实际输出调整后续节点配置
