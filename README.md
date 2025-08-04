# AI 塔罗牌占卜应用

这是一个基于PyQt5和OpenAI API的塔罗牌占卜应用程序。用户可以输入问题，抽取塔罗牌，并获得AI生成的专业解读。

## 功能特点
- 随机抽取塔罗牌（1-10张）
- 显示牌面信息和基本含义
- 通过OpenAI API获取深度解读
- 保存和查看历史记录
- 优雅的用户界面设计

## 技术栈
- Python 3.8+
- PyQt5: 用于创建GUI界面
- OpenAI API: 用于生成塔罗牌解读

## 安装指南

### 1. 克隆或下载代码
将代码保存到本地文件夹。

### 2. 安装依赖
使用pip安装所需的依赖包：
```bash
pip install -r requirements.txt
```

### 3. 配置OpenAI API密钥
在`aiiapp.py`文件中，替换以下行中的API密钥：
```python
OPENAI_API_KEY = "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"  # 请替换为您的API密钥
```

### 4. 运行应用
```bash
python aiiapp.py
```

## 打包指南
以下是将应用打包为Windows可执行文件(.exe)的步骤：

### 1. 安装PyInstaller
```bash
pip install pyinstaller
```

### 2. 准备图标文件（可选）
如果您想为应用添加图标，请准备一个.ico格式的图标文件，并命名为`tarot_icon.ico`，放在与`aiiapp.py`相同的目录下。

### 3. 执行打包命令
在命令行中，切换到应用所在的目录，然后执行以下命令：
```bash
pyinstaller --onefile --windowed --icon=tarot_icon.ico aiiapp.py
```

参数说明：
- `--onefile`: 生成单个可执行文件
- `--windowed`: 不显示控制台窗口
- `--icon`: 指定应用图标

### 4. 查找打包后的文件
打包完成后，可执行文件将位于`dist`目录下。

## 注意事项
- 应用需要访问互联网才能使用OpenAI API功能
- 请确保您的OpenAI API密钥有效且有足够的余额
- 历史记录保存在应用目录下的`history.json`文件中

## 版本更新记录
- v1.0: 初始版本，实现基本功能
- v1.1: 添加历史记录功能
- v1.2: 优化AI提示词，提升解读质量