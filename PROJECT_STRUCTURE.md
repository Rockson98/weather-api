# 📁 项目文件结构说明

## 🎯 核心功能文件

### 主应用
- **`main.py`** - Flask应用入口，启动天气API服务
- **`requirements.txt`** - Python依赖包列表
- **`render.yaml`** - Render云平台部署配置

### 天气API核心
- **`tianqi_webtool/`** - 天气工具包目录
  - `server.py` - Flask服务器实现
  - `client.py` - 天气数据客户端
  - `config.py` - 配置管理
  - `schemas.py` - 数据模型定义
  - `openweather_client.py` - OpenWeather API客户端
  - `__init__.py` - 包初始化文件

### Dify工具集成
- **`dify_tool/`** - Dify平台工具配置
  - `manifest.json` - 工具清单文件
  - `openapi.json` - OpenAPI规范文档
  - `weather_tool.py` - 工具实现代码

## 🔄 Dify多支路工作流方案

### 方案B：多支路工作流（推荐）
- **`dify_solution_b_main_processor.py`** - 主数据处理节点
  - 处理天气API数据
  - 为三个支路准备数据
  - 支持多种参数传递方式

- **`dify_solution_b_branch1_weather.py`** - 天气播报支路
  - 生成专业天气播报
  - 格式化天气信息
  - 输出播报内容

- **`dify_solution_b_branch2_prose.py`** - 散文生成支路
  - 基于天气数据创作散文
  - 生成文学性内容
  - 输出散文提示词和上下文

- **`dify_solution_b_data_merger.py`** - 数据合并节点
  - 合并各支路输出
  - 构建完整LLM提示词
  - 为LLM节点准备数据

## 📚 文档文件

### 主要文档
- **`README.md`** - 项目主文档，包含完整使用指南
- **`DIFY_INTEGRATION_GUIDE.md`** - Dify集成详细指南
- **`PROJECT_STRUCTURE.md`** - 本文件，项目结构说明

### 配置指南
- **`dify_solution_b_setup_guide.md`** - 多支路工作流配置指南
- **`dify_solution_b_llm_config_guide.md`** - LLM节点配置指南

## 🗂️ 文件分类

### 核心功能（必须保留）
```
main.py                          # 应用入口
tianqi_webtool/                  # 天气API核心
dify_tool/                       # Dify工具配置
requirements.txt                 # 依赖管理
render.yaml                      # 部署配置
README.md                        # 主文档
```

### Dify工作流（按需使用）
```
dify_solution_b_main_processor.py    # 主处理节点
dify_solution_b_branch1_weather.py   # 天气播报支路
dify_solution_b_branch2_prose.py     # 散文生成支路
dify_solution_b_data_merger.py       # 数据合并节点
```

### 配置文档（参考使用）
```
dify_solution_b_setup_guide.md       # 工作流配置
dify_solution_b_llm_config_guide.md  # LLM配置
DIFY_INTEGRATION_GUIDE.md            # 集成指南
```

## 🚀 使用建议

### 简单集成
如果您只需要基本的天气查询功能：
- 使用 `main.py` 启动服务
- 参考 `README.md` 进行Dify集成
- 使用 `dify_tool/` 中的配置文件

### 高级工作流
如果您需要多支路工作流：
- 使用 `dify_solution_b_*.py` 文件
- 参考 `dify_solution_b_setup_guide.md` 配置
- 参考 `dify_solution_b_llm_config_guide.md` 配置LLM

## 🧹 已清理的文件

以下文件已被删除（过时或重复）：
- `dify_code_execution_*.py` - 过时的代码执行文件
- `dify_*_fix.py` - 临时修复文件
- `dify_multi_branch_workflow.py` - 重复的工作流文件
- `dify_solution_b_main_processor_simple.py` - 简化版处理器
- `README_DIFY.md` - 重复的README文件
- 各种临时脚本和调试文件

## 📋 维护清单

### 定期检查
- [ ] 确保核心功能文件完整
- [ ] 更新依赖包版本
- [ ] 检查文档的准确性
- [ ] 验证Dify集成配置

### 新增功能时
- [ ] 更新相关文档
- [ ] 保持文件命名规范
- [ ] 添加适当的注释
- [ ] 更新项目结构说明

## 🔍 故障排除

如果遇到问题，请检查：
1. 核心文件是否存在
2. 依赖是否正确安装
3. 环境变量是否配置
4. 文档是否最新
5. 文件权限是否正确
