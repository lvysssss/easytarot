"""
标题栏组件
实现无边框窗口的自定义标题栏，支持拖拽、最小化、最大化、关闭
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from gui.styles import TITLE_BAR_BUTTON_STYLE, CLOSE_BUTTON_STYLE, TITLE_BAR_STYLE


class DraggableTitleBar(QWidget):
    """可拖拽的自定义标题栏"""

    # 边框调整区域宽度（与主窗口一致）
    RESIZE_MARGIN = 8

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.setFixedHeight(48)
        self.setStyleSheet(TITLE_BAR_STYLE)
        self.setCursor(Qt.ArrowCursor)

        self.drag_position = None
        self.is_dragging = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 0, 0)
        layout.setSpacing(0)

        title_label = QLabel("AI 塔罗牌占卜")
        title_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title_label.setStyleSheet("color: #2D2D2D; background: transparent;")

        layout.addWidget(title_label)
        layout.addStretch()

        btn_size = 46

        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(btn_size, btn_size)
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.setStyleSheet(TITLE_BAR_BUTTON_STYLE)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)

        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(btn_size, btn_size)
        self.max_btn.setCursor(Qt.PointingHandCursor)
        self.max_btn.setStyleSheet(TITLE_BAR_BUTTON_STYLE)
        self.max_btn.clicked.connect(self.toggle_maximize)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(btn_size, btn_size)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet(CLOSE_BUTTON_STYLE)
        self.close_btn.clicked.connect(self.parent_window.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent_window.showMaximized()
            self.max_btn.setText("❐")

    def _is_in_resize_zone(self, pos):
        """检查是否在调整大小区域"""
        x = pos.x()
        return x <= self.RESIZE_MARGIN or x >= self.width() - self.RESIZE_MARGIN

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 如果在边框调整区域，不处理，让父窗口处理
            if self._is_in_resize_zone(event.pos()):
                event.ignore()
                return

            child = self.childAt(event.pos())
            if isinstance(child, QPushButton):
                event.ignore()
                return

            self.drag_position = event.globalPos() - self.parent_window.frameGeometry().topLeft()
            self.is_dragging = True
            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.drag_position:
            if self.parent_window.isMaximized():
                self.parent_window.showNormal()
                self.max_btn.setText("□")

            new_pos = event.globalPos() - self.drag_position

            screen = QApplication.desktop().screenGeometry()
            window_geometry = self.parent_window.frameGeometry()

            min_x = 0
            min_y = 0
            max_x = screen.width() - window_geometry.width()
            max_y = screen.height() - window_geometry.height()

            new_pos.setX(max(min_x, min(new_pos.x(), max_x)))
            new_pos.setY(max(min_y, min(new_pos.y(), max_y)))

            self.parent_window.move(new_pos)
            event.accept()
        else:
            # 不在拖拽状态时，检查是否在边框区域，设置相应光标
            if self._is_in_resize_zone(event.pos()):
                # 让父窗口处理光标
                event.ignore()
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.drag_position = None
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()