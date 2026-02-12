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

class ModernCardWidget(QWidget):
    def __init__(self, card, index, parent=None):
        super().__init__(parent)
        self.card = card
        self.index = index
        
        self.setFixedSize(200, 320)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        self.setStyleSheet("""
            ModernCardWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(45, 27, 78, 0.9),
                    stop:0.5 rgba(76, 29, 149, 0.9),
                    stop:1 rgba(45, 27, 78, 0.9));
                border-radius: 20px;
                border: 2px solid rgba(251, 191, 36, 0.3);
            }
            ModernCardWidget:hover {
                border: 2px solid rgba(251, 191, 36, 0.8);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        card_number = QLabel(f"#{self.index}")
        card_number.setFont(QFont("Segoe UI", 10))
        card_number.setStyleSheet("color: rgba(251, 191, 36, 0.6);")
        card_number.setAlignment(Qt.AlignRight)
        
        title_label = QLabel(self.card.name)
        title_font = QFont("Segoe UI", 13, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #fbbf24;")
        
        orientation_label = QLabel(self.card.orientation)
        orientation_font = QFont("Segoe UI", 10, QFont.Bold)
        orientation_label.setFont(orientation_font)
        orientation_label.setAlignment(Qt.AlignCenter)
        
        if self.card.orientation == "正位":
            orientation_label.setStyleSheet("color: #34d399; padding: 4px 12px; background: rgba(52, 211, 153, 0.2); border-radius: 12px;")
        else:
            orientation_label.setStyleSheet("color: #f87171; padding: 4px 12px; background: rgba(248, 113, 113, 0.2); border-radius: 12px;")
        
        suit_label = QLabel(f"花色: {self.card.suit if self.card.suit else '大阿卡纳'}")
        suit_label.setFont(QFont("Segoe UI", 9))
        suit_label.setAlignment(Qt.AlignCenter)
        suit_label.setStyleSheet("color: rgba(251, 191, 36, 0.7);")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(251, 191, 36, 0.3);")
        
        meaning_label = QLabel(self.card.meaning)
        meaning_label.setFont(QFont("Segoe UI", 9))
        meaning_label.setWordWrap(True)
        meaning_label.setAlignment(Qt.AlignCenter)
        meaning_label.setStyleSheet("color: #e2e8f0; line-height: 1.4;")
        
        layout.addWidget(card_number)
        layout.addWidget(title_label)
        layout.addWidget(orientation_label)
        layout.addWidget(suit_label)
        layout.addWidget(separator)
        layout.addWidget(meaning_label)
        
        self.setLayout(layout)
    
    def setup_animations(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(25)
        self.shadow_effect.setColor(QColor(251, 191, 36, 100))
        self.shadow_effect.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow_effect)
    
    def enterEvent(self, event):
        self.shadow_effect.setBlurRadius(40)
        self.shadow_effect.setColor(QColor(251, 191, 36, 180))
        self.shadow_effect.setOffset(0, 12)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.shadow_effect.setBlurRadius(25)
        self.shadow_effect.setColor(QColor(251, 191, 36, 100))
        self.shadow_effect.setOffset(0, 8)
        super().leaveEvent(event)

class ModernHistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setGeometry(200, 200, 900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.history = history
        self.init_ui()
        self.setup_animations()
    
    def init_ui(self):
        main_container = QWidget()
        main_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(17, 24, 39, 0.95),
                    stop:1 rgba(31, 41, 55, 0.95));
                border-radius: 24px;
                border: 1px solid rgba(251, 191, 36, 0.2);
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("历史占卜记录")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #fbbf24;")
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.2);
                color: #ef4444;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.4);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background: rgba(17, 24, 39, 0.6);
                border: 1px solid rgba(251, 191, 36, 0.2);
                border-radius: 16px;
                padding: 10px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 10px;
                margin: 5px;
                color: #e2e8f0;
                background: rgba(251, 191, 36, 0.05);
            }
            QListWidget::item:hover {
                background: rgba(251, 191, 36, 0.15);
            }
            QListWidget::item:selected {
                background: rgba(251, 191, 36, 0.25);
                border: 1px solid rgba(251, 191, 36, 0.4);
            }
            QListWidget::item:selected:!active {
                background: rgba(251, 191, 36, 0.2);
            }
        """)
        self.history_list.setFixedWidth(350)
        
        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"📅 {item['timestamp']}\n❓ {item['question'][:35]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)
        
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        detail_container = QWidget()
        detail_container.setStyleSheet("""
            QWidget {
                background: rgba(17, 24, 39, 0.6);
                border-radius: 16px;
                border: 1px solid rgba(251, 191, 36, 0.2);
            }
        """)
        
        detail_layout = QVBoxLayout()
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(15)
        
        section_title = QLabel("解读详情")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        section_title.setStyleSheet("color: #fbbf24;")
        
        self.question_label = QLabel("问题:")
        self.question_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.question_label.setStyleSheet("color: #fbbf24;")
        self.question_content = QLabel("")
        self.question_content.setWordWrap(True)
        self.question_content.setStyleSheet("color: #e2e8f0; padding: 10px; background: rgba(251, 191, 36, 0.05); border-radius: 8px;")
        
        self.cards_label = QLabel("抽取的牌:")
        self.cards_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cards_label.setStyleSheet("color: #fbbf24;")
        self.cards_content = QLabel("")
        self.cards_content.setWordWrap(True)
        self.cards_content.setStyleSheet("color: #e2e8f0; padding: 10px; background: rgba(251, 191, 36, 0.05); border-radius: 8px;")
        
        self.analysis_label = QLabel("解读结果:")
        self.analysis_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.analysis_label.setStyleSheet("color: #fbbf24;")
        self.analysis_content = QTextEdit()
        self.analysis_content.setReadOnly(True)
        self.analysis_content.setStyleSheet("""
            QTextEdit {
                background: rgba(17, 24, 39, 0.8);
                border: 1px solid rgba(251, 191, 36, 0.2);
                border-radius: 12px;
                padding: 15px;
                color: #e2e8f0;
                font-size: 13px;
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
        
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("🗑️ 删除选中")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(239, 68, 68, 0.8),
                    stop:1 rgba(220, 38, 38, 0.8));
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(239, 68, 68, 1),
                    stop:1 rgba(220, 38, 38, 1));
            }
        """)
        self.delete_button.clicked.connect(self.delete_history_item)
        
        self.copy_button = QPushButton("📋 复制信息")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(251, 191, 36, 0.8),
                    stop:1 rgba(245, 158, 11, 0.8));
                color: #1f2937;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(251, 191, 36, 1),
                    stop:1 rgba(245, 158, 11, 1));
            }
        """)
        self.copy_button.clicked.connect(self.copy_history_info)
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(button_layout)
        
        main_container.setLayout(main_layout)
        
        dialog_layout = QVBoxLayout()
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(main_container)
        
        self.setLayout(dialog_layout)
    
    def setup_animations(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(50)
        self.shadow_effect.setColor(QColor(0, 0, 0, 150))
        self.shadow_effect.setOffset(0, 10)
        self.setGraphicsEffect(self.shadow_effect)
    
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
            list_item = QListWidgetItem(f"📅 {item['timestamp']}\n❓ {item['question'][:35]}...")
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(45, 27, 78, 0.7),
                    stop:1 rgba(76, 29, 149, 0.7));
                border-radius: 20px;
                border: 2px solid rgba(251, 191, 36, 0.3);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("✨")
        icon_label.setFont(QFont("Segoe UI", 24))
        
        title_label = QLabel("AI 智慧解读")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #fbbf24;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Segoe UI", 11))
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background: rgba(17, 24, 39, 0.6);
                border: 1px solid rgba(251, 191, 36, 0.2);
                border-radius: 16px;
                padding: 20px;
                color: #e2e8f0;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border: 1px solid rgba(251, 191, 36, 0.5);
            }
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.analysis_text)
        
        self.setLayout(layout)
        self.worker = None
    
    def set_analysis(self, question, cards, callback=None):
        self.analysis_text.setText("🔮 正在连接宇宙能量，生成AI解读，请稍候...")
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
        self.analysis_text.setText(f"❌ {error_message}")
        if hasattr(self, 'callback') and self.callback:
            self.callback(None, error_message)

class ModernTarotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 塔罗牌占卜")
        self.setGeometry(100, 100, 1200, 900)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.init_ui()
        self.setup_animations()
        
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
        except Exception as e:
            print(f"加载历史记录失败: {str(e)}")
            self.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {str(e)}")
    
    def show_history(self):
        history_dialog = ModernHistoryDialog(self.history, self)
        history_dialog.exec_()
    
    def init_ui(self):
        main_container = QWidget()
        main_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(17, 24, 39, 0.98),
                    stop:0.5 rgba(31, 41, 55, 0.98),
                    stop:1 rgba(17, 24, 39, 0.98));
                border-radius: 24px;
                border: 1px solid rgba(251, 191, 36, 0.2);
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        title_bar = self.create_title_bar()
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        title_label = QLabel("✨ AI 塔罗牌占卜 ✨")
        title_font = QFont("Segoe UI", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fbbf24,
                stop:0.5 #f59e0b,
                stop:1 #fbbf24);
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("🔮 输入您的问题，让塔罗牌揭示宇宙的智慧")
        subtitle_font = QFont("Segoe UI", 13)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: rgba(251, 191, 36, 0.7);")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        question_group = QGroupBox()
        question_group.setStyleSheet("""
            QGroupBox {
                background: rgba(17, 24, 39, 0.6);
                border: 2px solid rgba(251, 191, 36, 0.3);
                border-radius: 20px;
                margin-top: 10px;
                font-size: 14px;
                font-weight: bold;
                color: #fbbf24;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        question_group.setTitle("🤔 您的问题")
        
        question_layout = QVBoxLayout()
        question_layout.setContentsMargins(20, 25, 20, 20)
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入您想询问的问题...")
        self.question_input.setStyleSheet("""
            QLineEdit {
                background: rgba(17, 24, 39, 0.8);
                border: 2px solid rgba(251, 191, 36, 0.3);
                border-radius: 16px;
                padding: 16px 20px;
                font-size: 14px;
                color: #e2e8f0;
            }
            QLineEdit:focus {
                border: 2px solid rgba(251, 191, 36, 0.8);
                background: rgba(17, 24, 39, 0.9);
            }
            QLineEdit::placeholder {
                color: rgba(251, 191, 36, 0.4);
            }
        """)
        self.question_input.setMinimumHeight(50)
        
        question_layout.addWidget(self.question_input)
        question_group.setLayout(question_layout)
        
        control_layout = QHBoxLayout()
        control_layout.setSpacing(15)
        
        self.history_button = QPushButton("📜 历史记录")
        self.history_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.history_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 29, 149, 0.8),
                    stop:1 rgba(107, 33, 168, 0.8));
                color: white;
                border: none;
                border-radius: 14px;
                padding: 14px 28px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 29, 149, 1),
                    stop:1 rgba(107, 33, 168, 1));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 29, 149, 0.6),
                    stop:1 rgba(107, 33, 168, 0.6));
            }
        """)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setCursor(Qt.PointingHandCursor)
        
        self.copy_button = QPushButton("📋 复制牌面")
        self.copy_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.copy_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 29, 149, 0.8),
                    stop:1 rgba(107, 33, 168, 0.8));
                color: white;
                border: none;
                border-radius: 14px;
                padding: 14px 28px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(76, 29, 149, 1),
                    stop:1 rgba(107, 33, 168, 1));
            }
            QPushButton:disabled {
                background: rgba(75, 85, 99, 0.5);
                color: rgba(229, 231, 235, 0.5);
            }
        """)
        self.copy_button.clicked.connect(self.copy_cards_info)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setEnabled(False)
        
        count_container = QWidget()
        count_container.setStyleSheet("""
            QWidget {
                background: rgba(17, 24, 39, 0.6);
                border-radius: 14px;
                border: 1px solid rgba(251, 191, 36, 0.3);
            }
        """)
        count_layout = QHBoxLayout()
        count_layout.setContentsMargins(15, 12, 15, 12)
        count_layout.setSpacing(10)
        
        count_label = QLabel("抽牌数量:")
        count_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        count_label.setStyleSheet("color: #fbbf24;")
        
        self.card_count = QComboBox()
        self.card_count.setStyleSheet("""
            QComboBox {
                background: rgba(17, 24, 39, 0.8);
                border: 2px solid rgba(251, 191, 36, 0.3);
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 13px;
                color: #e2e8f0;
                min-width: 80px;
            }
            QComboBox:focus {
                border: 2px solid rgba(251, 191, 36, 0.8);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #fbbf24;
            }
            QComboBox QAbstractItemView {
                background: rgba(17, 24, 39, 0.95);
                border: 2px solid rgba(251, 191, 36, 0.3);
                border-radius: 10px;
                selection-background-color: rgba(251, 191, 36, 0.3);
                selection-color: #fbbf24;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 15px;
                color: #e2e8f0;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: rgba(251, 191, 36, 0.2);
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
        
        self.draw_button = QPushButton("🎴 抽取塔罗牌")
        self.draw_button.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.draw_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(251, 191, 36, 0.9),
                    stop:0.5 rgba(245, 158, 11, 0.9),
                    stop:1 rgba(251, 191, 36, 0.9));
                color: #1f2937;
                border: none;
                border-radius: 14px;
                padding: 14px 32px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(251, 191, 36, 1),
                    stop:0.5 rgba(245, 158, 11, 1),
                    stop:1 rgba(251, 191, 36, 1));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(251, 191, 36, 0.7),
                    stop:0.5 rgba(245, 158, 11, 0.7),
                    stop:1 rgba(251, 191, 36, 0.7));
            }
        """)
        self.draw_button.clicked.connect(self.draw_cards)
        self.draw_button.setCursor(Qt.PointingHandCursor)
        
        control_layout.addWidget(self.history_button)
        control_layout.addWidget(self.copy_button)
        control_layout.addWidget(count_container)
        control_layout.addWidget(self.draw_button)
        
        cards_label = QLabel("🎴 抽取的塔罗牌")
        cards_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        cards_label.setStyleSheet("color: #fbbf24;")
        
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(17, 24, 39, 0.5);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(251, 191, 36, 0.4);
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(251, 191, 36, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: rgba(17, 24, 39, 0.5);
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(251, 191, 36, 0.4);
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(251, 191, 36, 0.6);
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(25)
        self.cards_container.setLayout(self.cards_layout)
        self.cards_scroll.setWidget(self.cards_container)
        self.cards_scroll.setMinimumHeight(360)
        
        self.analysis_widget = ModernAIAnalysisWidget()
        self.analysis_widget.setMinimumHeight(280)
        
        main_layout.addWidget(title_bar)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(question_group)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(cards_label)
        main_layout.addWidget(self.cards_scroll)
        main_layout.addWidget(self.analysis_widget)
        
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)
    
    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("AI 塔罗牌占卜")
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: rgba(251, 191, 36, 0.6);")
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.3);
                color: #ef4444;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.6);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(close_btn)
        
        title_bar.setLayout(layout)
        return title_bar
    
    def setup_animations(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(60)
        self.shadow_effect.setColor(QColor(0, 0, 0, 200))
        self.shadow_effect.setOffset(0, 15)
        self.centralWidget().setGraphicsEffect(self.shadow_effect)
    
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
            self.question_input.setPlaceholderText("⚠️ 请先输入您的问题...")
            return
        
        num_cards = int(self.card_count.currentText())
        
        for i in reversed(range(self.cards_layout.count())): 
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        self.deck = TarotDeck()
        self.drawn_cards = self.deck.draw(num_cards)
        
        for i, card in enumerate(self.drawn_cards, 1):
            card_widget = ModernCardWidget(card, i)
            self.cards_layout.addWidget(card_widget)
        
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
