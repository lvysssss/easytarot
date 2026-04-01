"""
GUI样式常量模块
集中管理所有样式，便于维护和主题切换
"""

# 颜色常量
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY_LIGHT = "#FAFAFA"
GRAY_BORDER = "#E0E0E0"
GRAY_TEXT = "#666666"
GRAY_PLACEHOLDER = "#999999"
GRAY_CONTENT = "#333333"
GRAY_HOVER = "#F0F0F0"
GRAY_PRESS = "#E0E0E0"
GRAY_SCROLL = "#F5F5F5"
GRAY_SCROLL_HANDLE = "#CCCCCC"
GRAY_SCROLL_HANDLE_HOVER = "#999999"

RED_CLOSE = "#E81123"
RED_CLOSE_PRESS = "#C50F1F"

# 字体
FONT_FAMILY = "Microsoft YaHei"

# 按钮样式
PRIMARY_BUTTON_STYLE = """
    QPushButton {
        background: #000000;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 0 24px;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #333333;
    }
    QPushButton:pressed {
        background: #666666;
    }
"""

SECONDARY_BUTTON_STYLE = """
    QPushButton {
        background: #FFFFFF;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 8px;
        padding: 0 24px;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #F0F0F0;
    }
    QPushButton:pressed {
        background: #E0E0E0;
    }
    QPushButton:disabled {
        background: #F5F5F5;
        color: #CCCCCC;
        border: 1px solid #E0E0E0;
    }
"""

CLOSE_BUTTON_STYLE = """
    QPushButton {
        background: transparent;
        color: #000000;
        border: none;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: #E81123;
        color: #FFFFFF;
    }
    QPushButton:pressed {
        background: #C50F1F;
        color: #FFFFFF;
    }
"""

TITLE_BAR_BUTTON_STYLE = """
    QPushButton {{
        background: transparent;
        color: #000000;
        border: none;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background: #E5E5E5;
    }}
    QPushButton:pressed {{
        background: #D0D0D0;
    }}
"""

# 输入框样式
INPUT_STYLE = """
    QLineEdit {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 13px;
        color: #333333;
    }
    QLineEdit:focus {
        border: 2px solid #000000;
    }
    QLineEdit::placeholder {
        color: #999999;
    }
"""

# 下拉框样式
COMBOBOX_STYLE = """
    QComboBox {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
        color: #333333;
        min-width: 60px;
    }
    QComboBox:focus {
        border: 2px solid #000000;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #000000;
    }
    QComboBox QAbstractItemView {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        selection-background-color: #000000;
        selection-color: #FFFFFF;
        padding: 4px;
    }
    QComboBox QAbstractItemView::item {
        padding: 8px 12px;
        color: #333333;
        border-radius: 4px;
    }
    QComboBox QAbstractItemView::item:hover {
        background: #F0F0F0;
    }
"""

# 文本编辑框样式
TEXT_EDIT_STYLE = """
    QTextEdit {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 12px;
        color: #333333;
        font-size: 12px;
    }
"""

# 滚动条样式
SCROLL_BAR_STYLE = """
    QScrollBar:vertical {
        background: #F5F5F5;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #CCCCCC;
        border-radius: 4px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background: #999999;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        background: #F5F5F5;
        height: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background: #CCCCCC;
        border-radius: 4px;
        min-width: 30px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #999999;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
"""

# 列表样式
LIST_WIDGET_STYLE = """
    QListWidget {
        background: #FAFAFA;
        border: 1px solid #E0E0E0;
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
        border: 1px solid #E0E0E0;
    }
    QListWidget::item:hover {
        background: #F0F0F0;
        border: 1px solid #000000;
    }
    QListWidget::item:selected {
        background: #000000;
        color: #FFFFFF;
        border: 1px solid #000000;
    }
"""

# 卡片容器样式
CARD_CONTAINER_STYLE = """
    QWidget {
        background: #FAFAFA;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
    }
"""

# 分组框样式
GROUP_BOX_STYLE = """
    QGroupBox {
        background: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        margin-top: 0;
        padding-top: 0;
    }
"""