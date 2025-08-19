# easytarot

## 项目概述
easytarot是一个基于Python和PyQt5开发的AI塔罗牌占卜应用，结合了传统塔罗牌的神秘智慧与现代AI的分析能力，为用户提供个性化的塔罗牌解读体验。

## 功能特点
- 支持抽取1-10张塔罗牌进行占卜
- 提供多种牌阵选择（单牌、三牌、五牌、七牌、十牌）
- 包含78张完整的塔罗牌（大阿卡纳和小阿卡纳）
- 每张牌都有详细的含义解释
- 基于OpenAI API的智能解读功能
- 历史记录保存与查看功能
- 复制牌面信息到剪贴板
- 美观友好的用户界面
- 流式AI分析输出，实时显示解读过程

## 项目结构
```
aiapp/
├── main.py             # 程序入口
├── tarot_deck.py       # 塔罗牌核心逻辑
├── gui.py              # 用户界面
├── ai_analysis.py      # AI分析功能
├── requirements.txt    # 项目依赖
├── .env                # 环境变量配置
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明
```

## 安装指南
1. 克隆或下载项目到本地
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   - 复制`.env.bak`为`.env`文件
   - 在`.env`文件中填入您的OpenAI API密钥和相关配置：
     ```
     OPENAI_API_KEY=your_api_key_here
     OPENAI_BASE_URL=https://api.openai.com/v1
     OPENAI_MODEL_NAME=gpt-3.5-turbo
     ```
4. 运行`main.py`启动应用：
   ```bash
   python main.py
   ```

## 使用方法
1. 在输入框中输入您的问题
2. 选择要抽取的牌数量（1/3/5/7/10张）
3. 点击"抽取塔罗牌"按钮
4. 等待AI分析完成后查看结果
5. 可以点击"历史记录"查看过往占卜结果
6. 可以点击"复制牌面"将牌面信息复制到剪贴板

## 牌阵说明
- **单牌**：适合简单问题，快速得到直接答案
- **三牌阵**：过去、现在、未来，适合大多数问题
- **五牌阵**：更详细的分析，适合复杂问题
- **七牌阵**：深入探讨问题的各个方面
- **十牌阵**：全面分析，适合重大决策

## 技术栈
- **前端界面**：PyQt5
- **AI分析**：OpenAI API
- **配置管理**：python-dotenv
- **多线程处理**：QThread

## 注意事项
- 本应用需要有效的OpenAI API密钥才能使用AI解读功能
- 请确保您的网络连接正常
- 塔罗牌解读仅供参考，请勿过分依赖
- 历史记录文件`tarot_history.json`会保存在项目根目录下

## 依赖项
- PyQt5==5.15.9
- openai>=1.0.0
- python-dotenv==1.0.1

## 许可证
本项目仅供学习和研究使用。

## 贡献
欢迎提交Issue和Pull Request来改进这个项目。
