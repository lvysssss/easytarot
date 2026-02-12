# 🔮 EasyTarot - AI塔罗牌占卜应用

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/PyQt5-5.15+-green.svg" alt="PyQt5">
  <img src="https://img.shields.io/badge/OpenAI-API-orange.svg" alt="OpenAI API">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

<p align="center">
  <b>结合传统塔罗智慧与现代AI技术的智能占卜应用</b>
</p>

---

## 📋 目录

- [项目概述](#-项目概述)
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [安装指南](#-安装指南)
- [使用方法](#-使用方法)
- [项目结构](#-项目结构)
- [API文档](#-api文档)
- [配置说明](#-配置说明)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)
- [联系方式](#-联系方式)

---

## 🎯 项目概述

**EasyTarot** 是一个基于 Python 开发的 AI 塔罗牌占卜应用，融合了传统塔罗牌的神秘智慧与现代人工智能的分析能力。应用提供图形界面(GUI)和命令行界面(CLI)两种使用方式，为用户提供个性化、智能化的塔罗牌解读体验。

### 核心亮点

- 🤖 **AI 智能解读** - 基于 OpenAI API 的深度学习分析
- 🎨 **双界面支持** - 美观的 GUI 和高效的 CLI 两种模式
- 🃏 **完整牌组** - 包含 78 张经典塔罗牌（22张大阿卡纳 + 56张小阿卡纳）
- 📊 **多种牌阵** - 支持 1/3/5/7/10 张牌的经典牌阵
- 💾 **历史记录** - 自动保存占卜历史，支持回顾分析

---

## ✨ 功能特性

### 🔮 占卜功能
- 支持抽取 1-10 张塔罗牌进行占卜
- 提供多种经典牌阵选择：
  - **单牌占卜** - 快速获取直接答案
  - **三牌阵** - 过去、现在、未来时间线分析
  - **五牌阵** - 深入探讨问题的多个维度
  - **七牌阵** - 全面解析问题各个方面
  - **十牌阵** - 凯尔特十字牌阵，适合重大决策

### 🤖 AI 分析
- 基于 OpenAI GPT 模型的智能解读
- 流式输出，实时显示分析过程
- 结合牌面正逆位、牌阵位置进行综合分析
- 个性化解读，针对用户具体问题给出建议

### 🖥️ 用户界面
- **GUI 模式**：现代化 PyQt5 界面，支持拖拽、动画效果
- **CLI 模式**：命令行交互，支持自动补全和历史记录
- 美观的卡片展示，支持牌面详情查看
- 一键复制占卜结果到剪贴板

### 💾 数据管理
- 自动保存占卜历史到本地 JSON 文件
- 支持查看、回顾过往占卜记录
- 历史记录包含时间戳、问题、牌阵和 AI 解读

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.7+ | 核心编程语言 |
| PyQt5 | 5.15+ | 图形用户界面 |
| OpenAI | 1.0+ | AI 分析引擎 |
| python-dotenv | 1.0+ | 环境变量管理 |
| prompt_toolkit | 3.0+ | CLI 增强（可选） |

---

## 📦 安装指南

### 环境要求

- Python 3.7 或更高版本
- 有效的 OpenAI API 密钥
- Windows 7/8/10/11、macOS 或 Linux

### 快速安装

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/easytarot.git
   cd easytarot
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   # 复制示例配置文件
   cp .env.bak .env
   
   # 编辑 .env 文件，填入你的 OpenAI API 密钥
   ```

4. **运行应用**
   ```bash
   # GUI 模式（默认）
   python main.py
   
   # CLI 模式
   python main.py --cli
   ```

### Windows 用户

项目提供 Windows 批处理启动脚本：

```bash
# 启动 GUI 版本
start_gui.bat

# 启动 CLI 版本
start_cli.bat

# 查看 CLI 帮助
start_cli.bat /?
```

---

## 🚀 使用方法

### GUI 模式

1. 启动应用后，在主界面输入你的问题
2. 选择要抽取的牌数量（1/3/5/7/10 张）
3. 点击「抽取塔罗牌」按钮
4. 等待 AI 分析完成，查看详细解读
5. 点击「历史记录」查看过往占卜
6. 点击「复制牌面」将结果复制到剪贴板

### CLI 模式

```bash
# 启动 CLI 交互模式
python main.py --cli

# 或直接运行 CLI 模块
python cli_main.py
```

**CLI 交互示例：**
```
🔮 欢迎来到 AI 塔罗牌占卜
请输入你的问题 (或输入 'quit' 退出): 我最近的运势如何?
请选择牌阵:
1. 单牌 - 快速直接答案
2. 三牌阵 - 过去、现在、未来
3. 五牌阵 - 深入分析
4. 七牌阵 - 全面探讨
5. 十牌阵 - 凯尔特十字
选择: 2

🎴 抽取的牌:
┌─────────────────┬─────────────────┬─────────────────┐
│ 1. 魔术师 (正位) │ 2. 月亮 (逆位)  │ 3. 太阳 (正位)  │
└─────────────────┴─────────────────┴─────────────────┘

🤖 AI 解读中...
[流式输出分析结果]
```

---

## 📁 项目结构

```
easytarot/
├── 📄 main.py                 # 程序入口，处理参数解析
├── 🖥️  gui.py                 # PyQt5 图形界面实现
├── 💻 cli_main.py             # 命令行界面实现
├── 🃏 tarot_deck.py          # 塔罗牌核心逻辑和数据
├── 🤖 ai_analysis.py         # OpenAI API 封装和分析
├── 📋 requirements.txt        # Python 依赖包列表
├── ⚙️  .env.bak               # 环境变量配置模板
├── 🚀 start_gui.bat          # Windows GUI 启动脚本
├── 🚀 start_cli.bat          # Windows CLI 启动脚本
├── 📖 README.md              # 项目说明文档
└── 📝 tarot_history.json     # 占卜历史记录（自动生成）
```

### 核心模块说明

| 文件 | 说明 |
|------|------|
| `main.py` | 应用程序入口，负责解析命令行参数并启动相应界面 |
| `gui.py` | 基于 PyQt5 的现代化图形界面，包含动画效果和主题 |
| `cli_main.py` | 命令行交互界面，支持 prompt_toolkit 增强 |
| `tarot_deck.py` | 塔罗牌数据结构和抽牌逻辑，包含 78 张牌定义 |
| `ai_analysis.py` | OpenAI API 封装，实现流式输出和多线程分析 |

---

## 📚 API 文档

### TarotDeck 类

塔罗牌核心类，管理牌组和抽牌逻辑。

```python
from tarot_deck import TarotDeck

# 创建牌组
deck = TarotDeck()

# 抽取指定数量的牌
cards = deck.draw(3)  # 抽取 3 张牌

# 获取单张牌信息
card = deck.get_card("愚者")
```

**主要方法：**

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `draw(n)` | `n: int` | `List[TarotCard]` | 抽取 n 张牌 |
| `get_card(name)` | `name: str` | `TarotCard` | 根据名称获取牌 |
| `reset()` | - | - | 重置牌组 |

### AIAnalysisWorker 类

AI 分析工作线程，基于 QThread 实现异步分析。

```python
from ai_analysis import AIAnalysisWorker

# 创建工作线程
worker = AIAnalysisWorker(question, cards, spread_type)

# 连接信号
worker.analysis_complete.connect(on_complete)
worker.analysis_chunk.connect(on_chunk)
worker.error_occurred.connect(on_error)

# 启动分析
worker.start()
```

**信号说明：**

| 信号 | 参数 | 说明 |
|------|------|------|
| `analysis_complete` | `result: str` | 分析完成时触发 |
| `analysis_chunk` | `chunk: str` | 流式输出时触发 |
| `error_occurred` | `error: str` | 发生错误时触发 |

---

## ⚙️ 配置说明

### 环境变量 (.env)

```ini
# OpenAI API 配置（必需）
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-3.5-turbo

# 可选配置
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000
```

### 配置项说明

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API 密钥 |
| `OPENAI_BASE_URL` | ❌ | `https://api.openai.com/v1` | API 基础 URL |
| `OPENAI_MODEL_NAME` | ❌ | `gpt-3.5-turbo` | 使用的模型 |
| `OPENAI_TEMPERATURE` | ❌ | `0.7` | 生成温度（0-2） |
| `OPENAI_MAX_TOKENS` | ❌ | `2000` | 最大生成令牌数 |

---

## 🤝 贡献指南

我们欢迎所有形式的贡献，包括但不限于：

- 🐛 提交 Bug 报告
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🎨 优化用户界面

### 贡献流程

1. **Fork 项目**
   - 点击 GitHub 页面的 Fork 按钮

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/yourusername/easytarot.git
   cd easytarot
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

5. **推送到分支**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **创建 Pull Request**
   - 在 GitHub 上提交 PR，描述你的更改

### 代码规范

- 遵循 PEP 8 Python 编码规范
- 添加适当的注释和文档字符串
- 确保代码通过基本测试
- 更新相关文档

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 EasyTarot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 📮 联系方式

- 📧 **Email**: your.email@example.com
- 🐙 **GitHub**: [https://github.com/yourusername/easytarot](https://github.com/yourusername/easytarot)
- 💬 **Issues**: [提交问题或建议](https://github.com/yourusername/easytarot/issues)

---

## 🙏 致谢

- 感谢 [OpenAI](https://openai.com/) 提供强大的 AI API
- 感谢 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 提供优秀的 GUI 框架
- 感谢所有贡献者和用户的支持

---

<p align="center">
  <b>⭐ 如果这个项目对你有帮助，请给它一个 Star！</b>
</p>

<p align="center">
  Made with ❤️ and 🔮
</p>
