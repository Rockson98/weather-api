"""
Dify Solution B - 数据合并节点
将天气播报和散文生成的数据合并，为LLM节点准备完整的提示词
"""

def main(*args, **kwargs):
    """
    合并天气播报和散文生成数据，构建完整的LLM提示词
    支持位置参数和关键字参数，兼容Dify的调用方式
    
    Args:
        *args: 位置参数，按顺序为：城市名称, 天气播报, 散文提示词, 散文上下文
        **kwargs: 关键字参数，支持多种参数名:
            - arg1/city/城市: 城市名称
            - arg2/weather_broadcast/天气播报: 天气播报内容
            - arg3/prose_prompt/散文提示词: 散文提示词
            - arg4/prose_context/散文上下文: 散文上下文
    
    Returns:
        dict: 包含合并后的提示词和相关数据
    """
    
    # 处理位置参数
    city = ""
    weather_broadcast = ""
    prose_prompt = ""
    prose_context = ""
    
    if len(args) > 0:
        city = args[0] or ""
    if len(args) > 1:
        weather_broadcast = args[1] or ""
    if len(args) > 2:
        prose_prompt = args[2] or ""
    if len(args) > 3:
        prose_context = args[3] or ""
    
    # 从kwargs中提取参数，支持多种参数名（覆盖位置参数）
    city = kwargs.get('arg1') or kwargs.get('city') or kwargs.get('城市') or city
    weather_broadcast = kwargs.get('arg2') or kwargs.get('weather_broadcast') or kwargs.get('天气播报') or weather_broadcast
    prose_prompt = kwargs.get('arg3') or kwargs.get('prose_prompt') or kwargs.get('散文提示词') or prose_prompt
    prose_context = kwargs.get('arg4') or kwargs.get('prose_context') or kwargs.get('散文上下文') or prose_context
    
    # 调试信息：打印接收到的参数
    debug_info = f"接收到的参数: {kwargs}"
    
    # 输入验证
    if not city or city.strip() == "":
        city = "未知城市"
    if not weather_broadcast or weather_broadcast.strip() == "":
        weather_broadcast = "暂无天气信息"
    if not prose_prompt or prose_prompt.strip() == "":
        prose_prompt = "请创作一段优美的天气散文"
    if not prose_context or prose_context.strip() == "":
        prose_context = "天气散文创作"
    
    # 构建完整的LLM提示词
    full_prompt = f"""你是一个专业的天气播报和文学创作助手。

## 当前任务
为{city}创作天气播报和散文。

## 天气播报
{weather_broadcast}

## 散文创作指导
{prose_prompt}

## 散文背景信息
{prose_context}

## 输出要求
请生成以下内容：

### 今日天气播报
[使用提供的天气播报内容，可以适当润色]

### 天气散文
[根据散文提示词创作一段200-300字的优美散文，体现城市特色和天气氛围]

## 写作要求
- 散文要富有诗意，描写生动
- 体现当前天气的特点和城市文化
- 语言流畅自然，情感真挚
- 营造身临其境的氛围感"""

    # 构建简化的上下文（用于调试）
    simple_context = f"城市：{city} | 天气：{weather_broadcast[:100]}... | 散文指导：{prose_prompt[:100]}..."
    
    return {
        "full_prompt": full_prompt,
        "city": city,
        "weather_broadcast": weather_broadcast,
        "prose_prompt": prose_prompt,
        "prose_context": prose_context,
        "simple_context": simple_context,
        "task_type": "weather_prose_creation",
        "output_format": "weather_broadcast + prose",
        "debug_info": debug_info
    }

def create_alternative_prompt(city, weather_broadcast, prose_prompt, prose_context):
    """
    创建备用的简化提示词（如果主提示词太长）
    """
    
    alternative_prompt = f"""为{city}创作天气播报和散文。

天气播报：{weather_broadcast}

散文指导：{prose_prompt}
散文背景：{prose_context}

输出格式：
### 今日天气播报
[播报内容]

### 天气散文
[创作散文]"""
    
    return {
        "alternative_prompt": alternative_prompt,
        "city": city,
        "task_type": "weather_prose_simple"
    }

def validate_inputs(city, weather_broadcast, prose_prompt, prose_context):
    """
    验证输入数据的完整性
    """
    errors = []
    
    if not city or city.strip() == "":
        errors.append("城市名称不能为空")
    
    if not weather_broadcast or weather_broadcast.strip() == "":
        errors.append("天气播报内容不能为空")
    
    if not prose_prompt or prose_prompt.strip() == "":
        errors.append("散文提示词不能为空")
    
    if not prose_context or prose_context.strip() == "":
        errors.append("散文上下文不能为空")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "input_count": 4,
        "valid_inputs": [city, weather_broadcast, prose_prompt, prose_context]
    }

# 主函数调用
if __name__ == "__main__":
    # 测试数据
    test_city = "北京"
    test_weather = "今日北京多云，气温25°C，体感温度28°C，湿度65%，东南风3级，能见度10公里。"
    test_prose_prompt = "为北京写一段关于多云天气的优美散文，体现初夏季节的舒适氛围。"
    test_prose_context = "北京，多云，25°C，体感28°C，初夏，上午"
    
    result = main(test_city, test_weather, test_prose_prompt, test_prose_context)
    print("=== 数据合并结果 ===")
    print(f"城市: {result['city']}")
    print(f"任务类型: {result['task_type']}")
    print(f"输出格式: {result['output_format']}")
    print(f"简化上下文: {result['simple_context']}")
    print("\n=== 完整提示词 ===")
    print(result['full_prompt'])
