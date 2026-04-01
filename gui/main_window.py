"""
主窗口模块
AI塔罗牌占卜应用的主界面
"""

import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QFrame, QComboBox,
    QScrollArea, QGroupBox, QGraphicsDropShadowEffect, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QClipboard, QCursor
from PyQt5.QtCore import Qt, QSize, QPoint, QRect

from tarot_deck import TarotDeck, TarotCard
from gui.widgets import (
    DraggableTitleBar,
    ModernCardWidget,
    ModernHistoryDialog,
    ModernAIAnalysisWidget,
)
from gui.styles import (
    PRIMARY_BUTTON_STYLE,
    SECONDARY_BUTTON_STYLE,
    INPUT_STYLE,
    COMBOBOX_STYLE,
    SCROLL_BAR_STYLE,
    GROUP_BOX_STYLE,
)


class ModernTarotApp(QMainWindow):
    """AI塔罗牌占卜主窗口"""

    # 边框调整大小的区域宽度
    RESIZE_MARGIN = 8

    # 最小窗口尺寸
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 塔罗牌占卜")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 窗口大小调整相关变量
        self._resize_direction = None
        self._resize_start_pos = None
        self._resize_start_geom = None
        self.setMouseTracking(True)

        self.init_ui()

        self.deck = TarotDeck()
        self.drawn_cards = []
        self.history = []
        self.history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tarot_history.json"
        )
        self.load_history()

    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {str(e)}")
            self.history = []

    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {str(e)}")

    def show_history(self):
        """显示历史记录对话框"""
        history_dialog = ModernHistoryDialog(self.history, self)
        history_dialog.exec_()

    def init_ui(self):
        """初始化UI界面"""
        main_container = QWidget()
        main_container.setStyleSheet("""
            QWidget {
                background: #FFFFFF;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title_bar = self.create_title_bar()

        content_widget = QWidget()
        content_widget.setStyleSheet("background: #FFFFFF;")

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 30, 40, 40)
        content_layout.setSpacing(24)

        # 头部标题
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel("AI 塔罗牌占卜")
        title_font = QFont("Microsoft YaHei", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #000000; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("输入您的问题，让塔罗牌揭示宇宙的智慧")
        subtitle_font = QFont("Microsoft YaHei", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666666; background: transparent;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        # 问题输入区
        question_group = QGroupBox()
        question_group.setStyleSheet(GROUP_BOX_STYLE)

        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(20, 20, 20, 20)

        question_title = QLabel("您的问题")
        question_title.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        question_title.setStyleSheet("color: #000000; background: transparent;")

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入您想询问的问题...")
        self.question_input.setStyleSheet(INPUT_STYLE)
        self.question_input.setMinimumHeight(48)

        question_layout.addWidget(question_title)
        question_layout.addWidget(self.question_input)
        question_group.setLayout(question_layout)

        # 控制按钮区
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        self.history_button = QPushButton("历史记录")
        self.history_button.setFixedHeight(44)
        self.history_button.setFont(QFont("Microsoft YaHei", 11))
        self.history_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setCursor(Qt.PointingHandCursor)

        self.copy_button = QPushButton("复制牌面")
        self.copy_button.setFixedHeight(44)
        self.copy_button.setFont(QFont("Microsoft YaHei", 11))
        self.copy_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.copy_button.clicked.connect(self.copy_cards_info)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setEnabled(False)

        # 抽牌数量选择
        count_container = QWidget()
        count_container.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        count_layout = QHBoxLayout()
        count_layout.setContentsMargins(16, 0, 16, 0)
        count_layout.setSpacing(10)

        count_label = QLabel("抽牌数量:")
        count_label.setFont(QFont("Microsoft YaHei", 11))
        count_label.setStyleSheet("color: #000000; background: transparent;")

        self.card_count = QComboBox()
        self.card_count.setStyleSheet(COMBOBOX_STYLE)

        self.card_count.addItem("1")
        self.card_count.setItemData(0, "单牌解读：适合简单问题，快速得到直接答案", Qt.ToolTipRole)
        self.card_count.addItem("3")
        self.card_count.setItemData(1, "三牌阵：过去、现在、未来，适合大多数问题", Qt.ToolTipRole)
        self.card_count.addItem("5")
        self.card_count.setItemData(2, "五牌阵：更详细的分析，适合复杂问题", Qt.ToolTipRole)
        self.card_count.addItem("7")
        self.card_count.setItemData(3, "七牌阵：深入探讨问题的各个方面", Qt.ToolTipRole)
        self.card_count.addItem("10")
        self.card_count.setItemData(4, "十牌阵：全面分析，适合重大决策", Qt.ToolTipRole)
        self.card_count.setCurrentIndex(1)

        count_layout.addWidget(count_label)
        count_layout.addWidget(self.card_count)
        count_container.setLayout(count_layout)
        count_container.setFixedHeight(44)

        self.draw_button = QPushButton("抽取塔罗牌")
        self.draw_button.setFixedHeight(44)
        self.draw_button.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.draw_button.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.draw_button.clicked.connect(self.draw_cards)
        self.draw_button.setCursor(Qt.PointingHandCursor)

        control_layout.addWidget(self.history_button)
        control_layout.addWidget(self.copy_button)
        control_layout.addWidget(count_container)
        control_layout.addWidget(self.draw_button)

        # 卡牌展示区
        cards_label = QLabel("抽取的塔罗牌")
        cards_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        cards_label.setStyleSheet("color: #000000; background: transparent;")

        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            {SCROLL_BAR_STYLE}
        """)

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(20)
        self.cards_layout.addStretch()
        self.cards_container.setLayout(self.cards_layout)
        self.cards_scroll.setWidget(self.cards_container)
        self.cards_scroll.setMinimumHeight(320)

        # AI分析区
        self.analysis_widget = ModernAIAnalysisWidget()
        self.analysis_widget.setMinimumHeight(240)

        content_layout.addLayout(header_layout)
        content_layout.addWidget(question_group)
        content_layout.addLayout(control_layout)
        content_layout.addWidget(cards_label)
        content_layout.addWidget(self.cards_scroll)
        content_layout.addWidget(self.analysis_widget)

        content_widget.setLayout(content_layout)

        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)

        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

    def create_title_bar(self):
        """创建标题栏"""
        return DraggableTitleBar(self)

    def copy_cards_info(self):
        """复制牌面信息到剪贴板"""
        question = self.question_input.text().strip()
        cards_info = [f"问题：{question}"]
        for i, card in enumerate(self.drawn_cards, 1):
            cards_info.append(f"第{i}张：{card.name} ({card.orientation})")

        cards_text = "\n".join(cards_info)
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)

    def draw_cards(self):
        """抽取塔罗牌并进行分析"""
        question = self.question_input.text().strip()
        if not question:
            self.question_input.setPlaceholderText("请先输入您的问题...")
            return

        num_cards = int(self.card_count.currentText())

        # 清除旧卡牌
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 创建新牌组并抽牌
        self.deck = TarotDeck()
        self.drawn_cards = self.deck.draw(num_cards)

        # 显示卡牌
        for i, card in enumerate(self.drawn_cards, 1):
            card_widget = ModernCardWidget(card, i)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card_widget)

        self.copy_button.setEnabled(True)

        # 保存历史记录回调
        def save_history_callback(analysis, error):
            if analysis:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cards_data = [
                    {
                        "name": card.name,
                        "suit": card.suit,
                        "orientation": card.orientation,
                        "meaning": card.meaning,
                    }
                    for card in self.drawn_cards
                ]

                history_item = {
                    "timestamp": timestamp,
                    "question": question,
                    "cards": cards_data,
                    "analysis": analysis,
                }
                self.history.append(history_item)
                self.save_history()

        # 启动AI分析
        self.analysis_widget.set_analysis(question, self.drawn_cards, save_history_callback)

    def _get_resize_direction(self, pos):
        """根据鼠标位置判断调整大小的方向"""
        rect = self.rect()
        x, y = pos.x(), pos.y()
        margin = self.RESIZE_MARGIN

        # 判断是否在边框调整区域
        on_left = x <= margin
        on_right = x >= rect.width() - margin
        on_top = y <= margin
        on_bottom = y >= rect.height() - margin

        # 返回调整方向
        if on_top and on_left:
            return "top_left"
        elif on_top and on_right:
            return "top_right"
        elif on_bottom and on_left:
            return "bottom_left"
        elif on_bottom and on_right:
            return "bottom_right"
        elif on_left:
            return "left"
        elif on_right:
            return "right"
        elif on_top:
            return "top"
        elif on_bottom:
            return "bottom"
        return None

    def _get_cursor_for_direction(self, direction):
        """根据调整方向返回对应的鼠标光标"""
        cursors = {
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "top_left": Qt.SizeFDiagCursor,
            "top_right": Qt.SizeBDiagCursor,
            "bottom_left": Qt.SizeBDiagCursor,
            "bottom_right": Qt.SizeFDiagCursor,
        }
        return cursors.get(direction, Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 更新光标或调整窗口大小"""
        if self._resize_direction and self._resize_start_pos:
            # 正在调整大小
            self._perform_resize(event.globalPos())
        else:
            # 更新光标样式
            direction = self._get_resize_direction(event.pos())
            if direction:
                self.setCursor(self._get_cursor_for_direction(direction))
            else:
                self.setCursor(Qt.ArrowCursor)

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """鼠标按下事件 - 开始调整大小"""
        if event.button() == Qt.LeftButton:
            direction = self._get_resize_direction(event.pos())
            if direction:
                self._resize_direction = direction
                self._resize_start_pos = event.globalPos()
                self._resize_start_geom = self.geometry()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件 - 结束调整大小"""
        if event.button() == Qt.LeftButton:
            self._resize_direction = None
            self._resize_start_pos = None
            self._resize_start_geom = None
            self.setCursor(Qt.ArrowCursor)

        super().mouseReleaseEvent(event)

    def _perform_resize(self, global_pos):
        """执行窗口大小调整"""
        if not self._resize_start_geom:
            return

        delta = global_pos - self._resize_start_pos
        geom = QRect(self._resize_start_geom)

        # 根据方向调整窗口
        if "left" in self._resize_direction:
            new_left = geom.left() + delta.x()
            new_width = geom.right() - new_left
            if new_width >= self.MIN_WIDTH:
                geom.setLeft(new_left)

        if "right" in self._resize_direction:
            new_width = geom.width() + delta.x()
            if new_width >= self.MIN_WIDTH:
                geom.setRight(geom.right() + delta.x())

        if "top" in self._resize_direction:
            new_top = geom.top() + delta.y()
            new_height = geom.bottom() - new_top
            if new_height >= self.MIN_HEIGHT:
                geom.setTop(new_top)

        if "bottom" in self._resize_direction:
            new_height = geom.height() + delta.y()
            if new_height >= self.MIN_HEIGHT:
                geom.setBottom(geom.bottom() + delta.y())

        self.setGeometry(geom)

    def leaveEvent(self, event):
        """鼠标离开窗口 - 恢复默认光标"""
        if not self._resize_direction:
            self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)


def main():
    """启动GUI应用"""
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ModernTarotApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()