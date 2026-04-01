"""
GUI样式常量模块
集中管理所有样式，便于维护和主题切换
灰色主题
"""

# 颜色常量 - 灰色主题
WHITE = "#F5F5F5"  # 主背景 - 浅灰
BLACK = "#2D2D2D"  # 主文字/按钮 - 深灰
GRAY_LIGHT = "#FAFAFA"
GRAY_BORDER = "#D0D0D0"
GRAY_TEXT = "#555555"
GRAY_PLACEHOLDER = "#888888"
GRAY_CONTENT = "#333333"
GRAY_HOVER = "#E8E8E8"
GRAY_PRESS = "#D8D8D8"
GRAY_SCROLL = "#ECECEC"
GRAY_SCROLL_HANDLE = "#B0B0B0"
GRAY_SCROLL_HANDLE_HOVER = "#909090"

# 强调色
ACCENT_COLOR = "#4A4A4A"
ACCENT_HOVER = "#5A5A5A"
ACCENT_PRESS = "#6A6A6A"

RED_CLOSE = "#DC3545"
RED_CLOSE_PRESS = "#C82333"

# 字体
FONT_FAMILY = "Microsoft YaHei"

# 按钮样式 - 主按钮
PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background: #3D3D3D;
        color: #F5F5F5;
        border: none;
        border-radius: 8px;
        padding: 0 24px;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #4D4D4D;
    }
    QPushButton:pressed {
        background: #5D5D5D;
    }
"""

# 次要按钮
SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background: #F5F5F5;
        color: #2D2D2D;
        border: 1px solid #C0C0C0;
        border-radius: 8px;
        padding: 0 24px;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #E8E8E8;
        border: 1px solid #A0A0A0;
    }
    QPushButton:pressed {
        background: #D8D8D8;
    }
    QPushButton:disabled {
        background: #ECECEC;
        color: #A0A0A0;
        border: 1px solid #D0D0D0;
    }
"""

CLOSE_BUTTON_STYLE = """
    QPushButton {
        background: transparent;
        color: #2D2D2D;
        border: none;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #DC3545;
        color: #FFFFFF;
    }
    QPushButton:pressed {
        background: #C82333;
        color: #FFFFFF;
    }
"""

TITLE_BAR_BUTTON_STYLE = """
    QPushButton {{
        background: transparent;
        color: #2D2D2D;
        border: none;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background: #D8D8D8;
    }}
    QPushButton:pressed {{
        background: #C8C8C8;
    }}
"""

# 输入框样式
INPUT_STYLE = """
    QLineEdit {
        background: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 13px;
        color: #333333;
    }
    QLineEdit:focus {
        border: 2px solid #3D3D3D;
    }
    QLineEdit::placeholder {
        color: #888888;
    }
"""

# 下拉框样式
COMBOBOX_STYLE = """
    QComboBox {
        background: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
        color: #333333;
        min-width: 60px;
    }
    QComboBox:focus {
        border: 2px solid #3D3D3D;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #3D3D3D;
    }
    QComboBox QAbstractItemView {
        background: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 6px;
        selection-background-color: #3D3D3D;
        selection-color: #FFFFFF;
        padding: 4px;
    }
    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        color: #333333;
        border-radius: 4px;
    }
    QComboBox QAbstractItemView::item:hover {
        background: #E8E8E8;
    }
"""

# 文本编辑框样式
TEXT_EDIT_STYLE = """
    QTextEdit {
        background: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 8px;
        padding: 12px;
        color: #333333;
        font-size: 12px;
    }
"""

# 滚动条样式
SCROLL_BAR_STYLE = """
    QScrollBar:vertical {
        background: #ECECEC;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #B0B0B0;
        border-radius: 4px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background: #909090;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        background: #ECECEC;
        height: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background: #B0B0B0;
        border-radius: 4px;
        min-width: 30px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #909090;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
"""

# 列表样式
LIST_WIDGET_STYLE = """
    QListWidget {
        background: #F0F0F0;
        border: 1px solid #D0D0D0;
        border-radius: 8px;
        padding: 8px;
        font-size: 12px;
    }
    QListWidget::item {
        padding: 12px;
        border-radius: 6px;
        margin: 4px;
        color: #333333;
        background: #FFFFFF;
        border: 1px solid #D0D0D0;
    }
    QListWidget::item:hover {
        background: #E8E8E8;
        border: 1px solid #A0A0A0;
    }
    QListWidget::item:selected {
        background: #3D3D3D;
        color: #FFFFFF;
        border: 1px solid #3D3D3D;
    }
"""

# 卡片容器样式
CARD_CONTAINER_STYLE = """
    QWidget {
        background: #F0F0F0;
        border-radius: 12px;
        border: 1px solid #D0D0D0;
    }
"""

# 分组框样式
GROUP_BOX_STYLE = """
    QGroupBox {
        background: #F0F0F0;
        border: 1px solid #D0D0D0;
        border-radius: 12px;
        margin-top: 0;
        padding-top: 0;
    }
"""

# 卡片样式
CARD_STYLE = """
    ModernCardWidget {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #D0D0D0;
    }
    ModernCardWidget:hover {
        border: 2px solid #3D3D3D;
    }
"""

# 标题栏样式
TITLE_BAR_STYLE = """
    QWidget {
        background: #F0F0F0;
        border: none;
    }
"""

# 主窗口背景
MAIN_BACKGROUND = "#F5F5F5"
CONTENT_BACKGROUND = "#F5F5F5"