# 🔮 EasyTarot - AI塔罗牌占卜应用

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
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

**EasyTarot** 是一个基于 Python 开发的 AI 塔罗牌占卜应用，融合了传统塔罗牌的神秘智慧与现代人工智能的分析能力。应用提供命令行界面(CLI)使用方式，为用户提供个性化、智能化的塔罗牌解读体验。

### 核心亮点

- 🤖 **AI 智能解读** - 基于 OpenAI API 的深度学习分析
- 💻 **CLI 界面** - 高效的命令行交互模式
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
- 支持自动抽牌和自选抽牌两种模式

### 🤖 AI 分析
- 基于 OpenAI GPT 模型的智能解读
- 流式输出，实时显示分析过程
- 结合牌面正逆位、牌阵位置进行综合分析
- 个性化解读，针对用户具体问题给出建议

### 💻 用户界面
- **CLI 模式**：命令行交互，支持自动补全和历史记录
- 美观的卡片展示，支持牌面详情查看

### 💾 数据管理
- 自动保存占卜历史到本地 JSON 文件
- 支持查看、回顾过往占卜记录
- 历史记录包含时间戳、问题、牌阵和 AI 解读

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.7+ | 核心编程语言 |
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
   python main.py
   ```

---

## 🚀 使用方法

### CLI 模式

```bash
# 启动 CLI 交互模式
python main.py

# 或直接运行 CLI 模块
python cli_main.py
```

**CLI 交互示例：**
```
=== AI 塔罗牌占卜 (CLI版本) ===
输入 '/quit' 或 '/exit' 退出程序
输入 '/history' 查看历史记录

==================================================
请输入命令或问题: 我最近的运势如何?
请选择抽牌数量 (1/3/5/7/10): 3
请选择抽牌模式 (1=自动模式, 2=自选模式): 1

问题: 我最近的运势如何?

抽取的塔罗牌:
第1张: 魔术师 (正位)
  基本含义: 创造力、意志力、显化能力
  具体解释: 你拥有强大的创造力和意志力，能够将想法转化为现实。这是一个开始新事物的绝佳时机。

第2张: 月亮 (逆位)
  基本含义: 释放恐惧、澄清困惑、潜意识浮现
  具体解释: 你正在摆脱内心的恐惧和困惑，真相逐渐浮出水面。保持警觉但不必过度担忧。

第3张: 太阳 (正位)
  基本含义: 成功、喜悦、活力、清晰
  具体解释: 成功和喜悦即将到来，你的努力将得到回报。保持积极乐观的态度。

正在生成AI解读，请稍候...
AI解读结果:
[AI 生成的详细解读]

是否复制牌面信息? (y/n):
```

**CLI 命令：**
- `/quit` 或 `/exit` - 退出程序
- `/history` - 查看历史记录

---

## 📁 项目结构

```
easytarot/
├── 📄 main.py                 # 程序入口
├── 💻 cli_main.py             # 命令行界面实现
├── 🃏 tarot_deck.py          # 塔罗牌核心逻辑和数据
├── 🤖 ai_analysis.py         # OpenAI API 封装和分析
├── 📋 requirements.txt        # Python 依赖包列表
├── ⚙️  .env.bak               # 环境变量配置模板
├── 📖 README.md              # 项目说明文档
└── 📝 tarot_history.json     # 占卜历史记录（自动生成）
```

### 核心模块说明

| 文件 | 说明 |
|------|------|
| `main.py` | 应用程序入口 |
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

# 根据序号抽取特定牌
cards = deck.draw_by_indices([1, 15, 30])  # 抽取第1、15、30张牌

# 获取单张牌信息
card = deck.get_card("愚者")
```

**主要方法：**

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `draw(n)` | `n: int` | `List[TarotCard]` | 抽取 n 张牌 |
| `draw_by_indices(indices)` | `indices: List[int]` | `List[TarotCard]` | 根据序号抽取牌 |
| `get_card(name)` | `name: str` | `TarotCard` | 根据名称获取牌 |
| `reset()` | - | - | 重置牌组 |

### AIAnalysisWorker 类

AI 分析工作器，基于标准线程实现异步分析。

```python
from ai_analysis import AIAnalysisWorker

# 创建工作器
worker = AIAnalysisWorker(question, cards)

# 设置回调函数
worker.on_update = lambda text: print(f"更新: {text}")
worker.on_complete = lambda text: print(f"完成: {text}")
worker.on_error = lambda error: print(f"错误: {error}")

# 启动分析
worker.start()
```

**回调函数说明：**

| 回调 | 参数 | 说明 |
|------|------|------|
| `on_update` | `text: str` | 流式输出时触发 |
| `on_complete` | `text: str` | 分析完成时触发 |
| `on_error` | `error: str` | 发生错误时触发 |

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
- 感谢所有贡献者和用户的支持

---

<p align="center">
  <b>⭐ 如果这个项目对你有帮助，请给它一个 Star！</b>
</p>

<p align="center">
  Made with ❤️ and 🔮
</p>
