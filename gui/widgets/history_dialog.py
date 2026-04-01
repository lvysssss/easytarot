"""
历史记录对话框
查看、删除、复制历史占卜记录
"""

from PyQt5.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QTextEdit, QMessageBox,
    QApplication
)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QPoint, QRect

from gui.styles import (
    PRIMARY_BUTTON_STYLE,
    SECONDARY_BUTTON_STYLE,
    CLOSE_BUTTON_STYLE,
    LIST_WIDGET_STYLE,
    BLACK,
    WHITE,
    GRAY_BORDER,
    GRAY_TEXT,
    GRAY_CONTENT,
    GRAY_LIGHT,
    GRAY_HOVER,
)


class ModernHistoryDialog(QDialog):
    """历史记录对话框"""

    # 边框调整大小的区域宽度
    RESIZE_MARGIN = 8

    # 最小窗口尺寸
    MIN_WIDTH = 600
    MIN_HEIGHT = 500

    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.history = history
        self.drag_position = None
        self.is_dragging = False

        # 窗口大小调整相关变量
        self._resize_direction = None
        self._resize_start_pos = None
        self._resize_start_geom = None
        self.setMouseTracking(True)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background: {WHITE};")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        title_bar = QWidget()
        title_bar.setFixedHeight(48)
        title_bar.setStyleSheet(f"background: {GRAY_LIGHT}; border-bottom: 1px solid {GRAY_BORDER};")

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(20, 0, 0, 0)

        title_label = QLabel("历史占卜记录")
        title_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {BLACK}; background: transparent;")

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(46, 46)
        close_btn.setStyleSheet(CLOSE_BUTTON_STYLE)
        close_btn.clicked.connect(self.close)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        title_bar.setLayout(title_layout)

        # 内容区域
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background: {WHITE};")

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # 历史列表
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(LIST_WIDGET_STYLE)
        self.history_list.setFixedWidth(320)

        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"{item['timestamp']}\n{item['question'][:40]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)

        self.history_list.itemClicked.connect(self.on_history_item_clicked)

        # 详情容器
        detail_container = QWidget()
        detail_container.setStyleSheet(f"""
            QWidget {{
                background: {GRAY_LIGHT};
                border-radius: 8px;
                border: 1px solid {GRAY_BORDER};
            }}
        """)

        detail_layout = QVBoxLayout()
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(12)

        section_title = QLabel("解读详情")
        section_title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        section_title.setStyleSheet(f"color: {BLACK}; background: transparent;")

        self.question_label = QLabel("问题:")
        self.question_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.question_label.setStyleSheet(f"color: {BLACK}; background: transparent;")
        self.question_content = QLabel("")
        self.question_content.setWordWrap(True)
        self.question_content.setStyleSheet(
            f"color: {GRAY_CONTENT}; padding: 10px; background: {WHITE}; "
            f"border-radius: 6px; border: 1px solid {GRAY_BORDER};"
        )

        self.cards_label = QLabel("抽取的牌:")
        self.cards_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.cards_label.setStyleSheet(f"color: {BLACK}; background: transparent;")
        self.cards_content = QLabel("")
        self.cards_content.setWordWrap(True)
        self.cards_content.setStyleSheet(
            f"color: {GRAY_CONTENT}; padding: 10px; background: {WHITE}; "
            f"border-radius: 6px; border: 1px solid {GRAY_BORDER};"
        )

        self.analysis_label = QLabel("解读结果:")
        self.analysis_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.analysis_label.setStyleSheet(f"color: {BLACK}; background: transparent;")
        self.analysis_content = QTextEdit()
        self.analysis_content.setReadOnly(True)
        self.analysis_content.setStyleSheet(f"""
            QTextEdit {{
                background: {WHITE};
                border: 1px solid {GRAY_BORDER};
                border-radius: 8px;
                padding: 12px;
                color: {GRAY_CONTENT};
                font-size: 12px;
            }}
        """)

        detail_layout.addWidget(section_title)
        detail_layout.addWidget(self.question_label)
        detail_layout.addWidget(self.question_content)
        detail_layout.addWidget(self.cards_label)
        detail_layout.addWidget(self.cards_content)
        detail_layout.addWidget(self.analysis_label)
        detail_layout.addWidget(self.analysis_content)

        detail_container.setLayout(detail_layout)

        content_layout.addWidget(self.history_list)
        content_layout.addWidget(detail_container)
        content_widget.setLayout(content_layout)

        # 按钮区域
        button_widget = QWidget()
        button_widget.setStyleSheet(f"background: {WHITE};")
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 10, 20, 20)

        self.delete_button = QPushButton("删除选中")
        self.delete_button.setFixedHeight(40)
        self.delete_button.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.delete_button.clicked.connect(self.delete_history_item)

        self.copy_button = QPushButton("复制信息")
        self.copy_button.setFixedHeight(40)
        self.copy_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.copy_button.clicked.connect(self.copy_history_info)

        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        button_widget.setLayout(button_layout)

        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 先检查是否在调整大小区域
            direction = self._get_resize_direction(event.pos())
            if direction:
                self._resize_direction = direction
                self._resize_start_pos = event.globalPos()
                self._resize_start_geom = self.geometry()
                event.accept()
                return

            # 否则检查是否可以拖拽移动
            child = self.childAt(event.pos())
            if isinstance(child, (QPushButton, QListWidget, QTextEdit)):
                event.ignore()
                return

            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.is_dragging = True
            event.accept()

    def mouseMoveEvent(self, event):
        # 如果正在调整大小
        if self._resize_direction and self._resize_start_pos:
            self._perform_resize(event.globalPos())
            event.accept()
            return

        # 如果正在拖拽移动
        if self.is_dragging and self.drag_position:
            new_pos = event.globalPos() - self.drag_position

            screen = QApplication.desktop().screenGeometry()
            window_geometry = self.frameGeometry()

            min_x = 0
            min_y = 0
            max_x = screen.width() - window_geometry.width()
            max_y = screen.height() - window_geometry.height()

            new_pos.setX(max(min_x, min(new_pos.x(), max_x)))
            new_pos.setY(max(min_y, min(new_pos.y(), max_y)))

            self.move(new_pos)
            event.accept()
            return

        # 更新光标样式
        direction = self._get_resize_direction(event.pos())
        if direction:
            self.setCursor(self._get_cursor_for_direction(direction))
        else:
            self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.drag_position = None
            self._resize_direction = None
            self._resize_start_pos = None
            self._resize_start_geom = None
            self.setCursor(Qt.ArrowCursor)
            event.accept()

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

    def on_history_item_clicked(self, item):
        index = item.data(Qt.UserRole)
        history_item = self.history[-(index + 1)]

        self.question_content.setText(history_item["question"])

        cards_text = "\n".join(
            [
                f"• {card['name']} ({card['orientation']}) - {card['meaning']}"
                for card in history_item["cards"]
            ]
        )
        self.cards_content.setText(cards_text)

        self.analysis_content.setText(history_item["analysis"])

    def delete_history_item(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要删除的记录")
            return

        for item in selected_items:
            index = item.data(Qt.UserRole)
            del self.history[-(index + 1)]

        self.history_list.clear()
        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"{item['timestamp']}\n{item['question'][:40]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)

        self.question_content.setText("")
        self.cards_content.setText("")
        self.analysis_content.setText("")

    def copy_history_info(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "请先选择要复制的记录")
            return

        item = selected_items[0]
        index = item.data(Qt.UserRole)
        history_item = self.history[-(index + 1)]

        cards_info = [f"问题：{history_item['question']}"]
        for i, card in enumerate(history_item["cards"], 1):
            cards_info.append(f"第{i}张：{card['name']} ({card['orientation']})")

        cards_text = "\n".join(cards_info)
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)

    def closeEvent(self, event):
        self.parent().save_history()
        event.accept()