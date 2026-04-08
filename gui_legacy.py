import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QFrame, QComboBox,
                             QScrollArea, QGroupBox, QListWidget, QListWidgetItem, QDialog, QMessageBox,
                             QGraphicsDropShadowEffect, QGridLayout, QSizePolicy)
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QColor, QPalette, QClipboard, QLinearGradient,
                         QBrush, QPen, QPainter, QRadialGradient, QPainterPath, QFontDatabase)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QPoint, QParallelAnimationGroup
from PyQt5.QtGui import QCursor
from tarot_deck import TarotDeck, TarotCard
from ai_analysis import AIAnalysisWorker

class DraggableTitleBar(QWidget):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.setFixedHeight(48)
        self.setStyleSheet("""
            QWidget {
                background: #FFFFFF;
                border: none;
            }
        """)
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
        title_label.setStyleSheet("color: #000000; background: transparent;")
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        btn_size = 46
        btn_style = """
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
        
        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(btn_size, btn_size)
        self.min_btn.setCursor(Qt.PointingHandCursor)
        self.min_btn.setStyleSheet(btn_style)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(btn_size, btn_size)
        self.max_btn.setCursor(Qt.PointingHandCursor)
        self.max_btn.setStyleSheet(btn_style)
        self.max_btn.clicked.connect(self.toggle_maximize)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(btn_size, btn_size)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
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
        """)
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
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
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
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.drag_position = None
            event.accept()
    
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle_maximize()

class ModernCardWidget(QWidget):
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
            orientation_label.setStyleSheet("color: #FFFFFF; padding: 6px 16px; background: #000000; border-radius: 16px;")
        else:
            orientation_label.setStyleSheet("color: #FFFFFF; padding: 6px 16px; background: #333333; border-radius: 16px;")
        
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
        meaning_label.setStyleSheet("color: #333333; background: transparent; line-height: 1.4;")
        
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

class ModernHistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setGeometry(200, 200, 900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.history = history
        self.drag_position = None
        self.is_dragging = False
        self.init_ui()
    
    def init_ui(self):
        self.setStyleSheet("background: #FFFFFF;")
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        title_bar = QWidget()
        title_bar.setFixedHeight(48)
        title_bar.setStyleSheet("background: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(20, 0, 0, 0)
        
        title_label = QLabel("历史占卜记录")
        title_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title_label.setStyleSheet("color: #000000; background: transparent;")
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(46, 46)
        close_btn.setStyleSheet("""
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
        """)
        close_btn.clicked.connect(self.close)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)
        title_bar.setLayout(title_layout)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #FFFFFF;")
        
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
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
        """)
        self.history_list.setFixedWidth(320)
        
        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"{item['timestamp']}\n{item['question'][:40]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)
        
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        detail_container = QWidget()
        detail_container.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        detail_layout = QVBoxLayout()
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(12)
        
        section_title = QLabel("解读详情")
        section_title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        section_title.setStyleSheet("color: #000000; background: transparent;")
        
        self.question_label = QLabel("问题:")
        self.question_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.question_label.setStyleSheet("color: #000000; background: transparent;")
        self.question_content = QLabel("")
        self.question_content.setWordWrap(True)
        self.question_content.setStyleSheet("color: #333333; padding: 10px; background: #FFFFFF; border-radius: 6px; border: 1px solid #E0E0E0;")
        
        self.cards_label = QLabel("抽取的牌:")
        self.cards_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.cards_label.setStyleSheet("color: #000000; background: transparent;")
        self.cards_content = QLabel("")
        self.cards_content.setWordWrap(True)
        self.cards_content.setStyleSheet("color: #333333; padding: 10px; background: #FFFFFF; border-radius: 6px; border: 1px solid #E0E0E0;")
        
        self.analysis_label = QLabel("解读结果:")
        self.analysis_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        self.analysis_label.setStyleSheet("color: #000000; background: transparent;")
        self.analysis_content = QTextEdit()
        self.analysis_content.setReadOnly(True)
        self.analysis_content.setStyleSheet("""
            QTextEdit {
                background: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
                color: #333333;
                font-size: 12px;
            }
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
        
        button_widget = QWidget()
        button_widget.setStyleSheet("background: #FFFFFF;")
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 10, 20, 20)
        
        self.delete_button = QPushButton("删除选中")
        self.delete_button.setFixedHeight(40)
        self.delete_button.setStyleSheet("""
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
        """)
        self.delete_button.clicked.connect(self.delete_history_item)
        
        self.copy_button = QPushButton("复制信息")
        self.copy_button.setFixedHeight(40)
        self.copy_button.setStyleSheet("""
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
        """)
        self.copy_button.clicked.connect(self.copy_history_info)
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        button_widget.setLayout(button_layout)
        
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)
        main_layout.addWidget(button_widget)
        
        self.setLayout(main_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            child = self.childAt(event.pos())
            if isinstance(child, QPushButton) or isinstance(child, QListWidget) or isinstance(child, QTextEdit):
                event.ignore()
                return
            
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.is_dragging = True
            event.accept()
    
    def mouseMoveEvent(self, event):
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
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.drag_position = None
            event.accept()
    
    def on_history_item_clicked(self, item):
        index = item.data(Qt.UserRole)
        history_item = self.history[-(index + 1)]
        
        self.question_content.setText(history_item['question'])
        
        cards_text = "\n".join([f"• {card['name']} ({card['orientation']}) - {card['meaning']}" for card in history_item['cards']])
        self.cards_content.setText(cards_text)
        
        self.analysis_content.setText(history_item['analysis'])
    
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
        for i, card in enumerate(history_item['cards'], 1):
            cards_info.append(f"第{i}张：{card['name']} ({card['orientation']})")
        
        cards_text = "\n".join(cards_info)
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)
    
    def closeEvent(self, event):
        self.parent().save_history()
        event.accept()

class ModernAIAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background: #FAFAFA;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("AI 智慧解读")
        title_font = QFont("Microsoft YaHei", 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #000000; background: transparent;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Microsoft YaHei", 11))
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 16px;
                color: #333333;
                line-height: 1.6;
            }
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.analysis_text)
        
        self.setLayout(layout)
        self.worker = None
    
    def set_analysis(self, question, cards, callback=None):
        self.analysis_text.setText("正在连接AI，生成解读，请稍候...")
        self.callback = callback
        
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
        
        self.worker = AIAnalysisWorker(question, cards)
        self.worker.analysis_update.connect(self.on_analysis_update)
        self.worker.analysis_complete.connect(self.on_analysis_complete)
        self.worker.analysis_error.connect(self.on_analysis_error)
        self.worker.start()
    
    def on_analysis_update(self, partial_text):
        self.analysis_text.setText(partial_text)
        self.analysis_text.verticalScrollBar().setValue(self.analysis_text.verticalScrollBar().maximum())
    
    def on_analysis_complete(self, analysis):
        self.analysis_text.setText(analysis)
        if hasattr(self, 'callback') and self.callback:
            self.callback(analysis, None)
    
    def on_analysis_error(self, error_message):
        self.analysis_text.setText(f"错误: {error_message}")
        if hasattr(self, 'callback') and self.callback:
            self.callback(None, error_message)

class ModernTarotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 塔罗牌占卜")
        self.setGeometry(100, 100, 1200, 900)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.init_ui()
        
        self.deck = TarotDeck()
        self.drawn_cards = []
        self.history = []
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tarot_history.json')
        self.load_history()
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def show_history(self):
        history_dialog = ModernHistoryDialog(self.history, self)
        history_dialog.exec_()
    
    def init_ui(self):
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
        
        question_group = QGroupBox()
        question_group.setStyleSheet("""
            QGroupBox {
                background: #FAFAFA;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                margin-top: 0;
                padding-top: 0;
            }
        """)
        
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(20, 20, 20, 20)
        
        question_title = QLabel("您的问题")
        question_title.setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        question_title.setStyleSheet("color: #000000; background: transparent;")
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入您想询问的问题...")
        self.question_input.setStyleSheet("""
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
        """)
        self.question_input.setMinimumHeight(48)
        
        question_layout.addWidget(question_title)
        question_layout.addWidget(self.question_input)
        question_group.setLayout(question_layout)
        
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)
        
        self.history_button = QPushButton("历史记录")
        self.history_button.setFixedHeight(44)
        self.history_button.setFont(QFont("Microsoft YaHei", 11))
        self.history_button.setStyleSheet("""
            QPushButton {
                background: #FFFFFF;
                color: #000000;
                border: 1px solid #000000;
                border-radius: 8px;
                padding: 0 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #F0F0F0;
            }
            QPushButton:pressed {
                background: #E0E0E0;
            }
        """)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setCursor(Qt.PointingHandCursor)
        
        self.copy_button = QPushButton("复制牌面")
        self.copy_button.setFixedHeight(44)
        self.copy_button.setFont(QFont("Microsoft YaHei", 11))
        self.copy_button.setStyleSheet("""
            QPushButton {
                background: #FFFFFF;
                color: #000000;
                border: 1px solid #000000;
                border-radius: 8px;
                padding: 0 20px;
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
        """)
        self.copy_button.clicked.connect(self.copy_cards_info)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setEnabled(False)
        
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
        self.card_count.setStyleSheet("""
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
        """)
        
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
        self.draw_button.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #333333;
            }
            QPushButton:pressed {
                background: #666666;
            }
        """)
        self.draw_button.clicked.connect(self.draw_cards)
        self.draw_button.setCursor(Qt.PointingHandCursor)
        
        control_layout.addWidget(self.history_button)
        control_layout.addWidget(self.copy_button)
        control_layout.addWidget(count_container)
        control_layout.addWidget(self.draw_button)
        
        cards_label = QLabel("抽取的塔罗牌")
        cards_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        cards_label.setStyleSheet("color: #000000; background: transparent;")
        
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
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
        return DraggableTitleBar(self)
    
    def copy_cards_info(self):
        question = self.question_input.text().strip()
        cards_info = [f"问题：{question}"]
        for i, card in enumerate(self.drawn_cards, 1):
            cards_info.append(f"第{i}张：{card.name} ({card.orientation})")
        
        cards_text = "\n".join(cards_info)
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)
    
    def draw_cards(self):
        question = self.question_input.text().strip()
        if not question:
            self.question_input.setPlaceholderText("请先输入您的问题...")
            return
        
        num_cards = int(self.card_count.currentText())
        
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.deck = TarotDeck()
        self.drawn_cards = self.deck.draw(num_cards)
        
        for i, card in enumerate(self.drawn_cards, 1):
            card_widget = ModernCardWidget(card, i)
            self.cards_layout.insertWidget(self.cards_layout.count() - 1, card_widget)
        
        self.copy_button.setEnabled(True)
        
        def save_history_callback(analysis, error):
            if analysis:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cards_data = [{
                    'name': card.name,
                    'suit': card.suit,
                    'orientation': card.orientation,
                    'meaning': card.meaning
                } for card in self.drawn_cards]
                
                history_item = {
                    'timestamp': timestamp,
                    'question': question,
                    'cards': cards_data,
                    'analysis': analysis
                }
                self.history.append(history_item)
                self.save_history()
        
        self.analysis_widget.set_analysis(question, self.drawn_cards, save_history_callback)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ModernTarotApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
