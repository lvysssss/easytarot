"""
塔罗牌卡片组件
展示单张塔罗牌的信息卡片
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ModernCardWidget(QWidget):
    """塔罗牌卡片展示组件"""

    def __init__(self, card, index, parent=None):
        super().__init__(parent)
        self.card = card
        self.index = index

        self.setFixedSize(180, 280)
        self.setCursor(Qt.PointingHandCursor)

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            ModernCardWidget {
                background: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            ModernCardWidget:hover {
                border: 2px solid #000000;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        card_number = QLabel(f"#{self.index}")
        card_number.setFont(QFont("Microsoft YaHei", 10))
        card_number.setStyleSheet("color: #999999; background: transparent;")
        card_number.setAlignment(Qt.AlignRight)

        title_label = QLabel(self.card.name)
        title_font = QFont("Microsoft YaHei", 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #000000; background: transparent;")
        title_label.setWordWrap(True)

        orientation_label = QLabel(self.card.orientation)
        orientation_font = QFont("Microsoft YaHei", 10, QFont.Bold)
        orientation_label.setFont(orientation_font)
        orientation_label.setAlignment(Qt.AlignCenter)

        if self.card.orientation == "正位":
            orientation_label.setStyleSheet(
                "color: #FFFFFF; padding: 6px 16px; background: #000000; border-radius: 16px;"
            )
        else:
            orientation_label.setStyleSheet(
                "color: #FFFFFF; padding: 6px 16px; background: #333333; border-radius: 16px;"
            )

        suit_label = QLabel(f"花色: {self.card.suit if self.card.suit else '大阿卡纳'}")
        suit_label.setFont(QFont("Microsoft YaHei", 9))
        suit_label.setAlignment(Qt.AlignCenter)
        suit_label.setStyleSheet("color: #666666; background: transparent;")

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #E0E0E0;")
        separator.setFixedHeight(1)

        meaning_label = QLabel(self.card.meaning)
        meaning_label.setFont(QFont("Microsoft YaHei", 9))
        meaning_label.setWordWrap(True)
        meaning_label.setAlignment(Qt.AlignCenter)
        meaning_label.setStyleSheet(
            "color: #333333; background: transparent; line-height: 1.4;"
        )

        layout.addWidget(card_number)
        layout.addWidget(title_label)
        layout.addWidget(orientation_label)
        layout.addWidget(suit_label)
        layout.addWidget(separator)
        layout.addWidget(meaning_label)
        layout.addStretch()

        self.setLayout(layout)

    def enterEvent(self, event):
        self.setStyleSheet("""
            ModernCardWidget {
                background: #FFFFFF;
                border-radius: 12px;
                border: 2px solid #000000;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("""
            ModernCardWidget {
                background: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        super().leaveEvent(event)