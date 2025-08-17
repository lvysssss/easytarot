import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QFrame, QComboBox,
                             QScrollArea, QGroupBox, QListWidget, QListWidgetItem, QDialog, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QClipboard
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from tarot_deck import TarotDeck, TarotCard
from ai_analysis import AIAnalysisWorker

class CardWidget(QWidget):
    def __init__(self, card, parent=None):
        super().__init__(parent)
        self.card = card
        
        # 设置卡片样式
        self.setFixedSize(180, 300)
        self.setStyleSheet("""
            background-color: #f8f0e5;
            border-radius: 10px;
            border: 2px solid #d4a373;
            padding: 10px;
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 卡片标题
        title_label = QLabel(card.name)
        title_font = QFont("Arial", 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #432818;")
        
        # 卡片正逆位
        orientation_label = QLabel(card.orientation)
        orientation_font = QFont("Arial", 10)
        orientation_label.setFont(orientation_font)
        orientation_label.setAlignment(Qt.AlignCenter)
        
        # 设置不同颜色
        if card.orientation == "正位":
            orientation_label.setStyleSheet("color: #2a9d8f; font-weight: bold;")
        else:
            orientation_label.setStyleSheet("color: #e76f51; font-weight: bold;")
        
        # 花色标签
        suit_label = QLabel(f"花色: {card.suit if card.suit else '大阿卡纳'}")
        suit_label.setFont(QFont("Arial", 9))
        suit_label.setAlignment(Qt.AlignCenter)
        suit_label.setStyleSheet("color: #6c584c;")
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #d4a373;")
        
        # 含义标签
        meaning_label = QLabel(card.meaning)
        meaning_label.setFont(QFont("Arial", 9))
        meaning_label.setWordWrap(True)
        meaning_label.setAlignment(Qt.AlignCenter)
        meaning_label.setStyleSheet("color: #432818;")
        
        # 添加到布局
        layout.addWidget(title_label)
        layout.addWidget(orientation_label)
        layout.addWidget(suit_label)
        layout.addWidget(separator)
        layout.addWidget(meaning_label)
        
        self.setLayout(layout)

class HistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #f9f5f0;")
        
        self.history = history
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # 历史记录列表
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(""
            "QListWidget {background-color: #f8f0e5; border: 1px solid #d4a373; border-radius: 5px;}"
            "QListWidget::item {padding: 10px; border-bottom: 1px solid #d4a373;}"
            "QListWidget::item:selected {background-color: #e9d8c5; color: #432818;}"
        )
        
        # 填充历史记录
        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"{item['timestamp']} - {item['question'][:30]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)
        
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        # 详细信息区域
        self.detail_group = QGroupBox("解读详情")
        self.detail_group.setStyleSheet(""
            "QGroupBox {font-weight: bold; color: #432818; border: 2px solid #d4a373; border-radius: 10px; margin-top: 16px;}"
            "QGroupBox::title {subcontrol-origin: margin; left: 10px; padding: 0 5px;}"
        )
        
        detail_layout = QVBoxLayout()
        
        self.question_label = QLabel("问题:")
        self.question_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.question_content = QLabel("")
        self.question_content.setWordWrap(True)
        
        self.cards_label = QLabel("抽取的牌:")
        self.cards_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.cards_content = QLabel("")
        self.cards_content.setWordWrap(True)
        
        self.analysis_label = QLabel("解读结果:")
        self.analysis_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.analysis_content = QTextEdit()
        self.analysis_content.setReadOnly(True)
        self.analysis_content.setStyleSheet("background-color: #f8f0e5; border: 1px solid #d4a373; border-radius: 5px;")
        
        detail_layout.addWidget(self.question_label)
        detail_layout.addWidget(self.question_content)
        detail_layout.addWidget(self.cards_label)
        detail_layout.addWidget(self.cards_content)
        detail_layout.addWidget(self.analysis_label)
        detail_layout.addWidget(self.analysis_content)
        
        self.detail_group.setLayout(detail_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("删除选中记录")
        self.delete_button.setStyleSheet(
            "QPushButton {background-color: #d4a373; color: white; border-radius: 5px; padding: 5px 10px;}"
            "QPushButton:hover {background-color: #bc6c25;}"
        )
        self.delete_button.clicked.connect(self.delete_history_item)
        
        self.copy_button = QPushButton("复制牌面信息")
        self.copy_button.setStyleSheet(
            "QPushButton {background-color: #d4a373; color: white; border-radius: 5px; padding: 5px 10px;}"
            "QPushButton:hover {background-color: #bc6c25;}"
        )
        self.copy_button.clicked.connect(self.copy_history_info)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        
        self.close_button = QPushButton("关闭")
        self.close_button.setStyleSheet(
            "QPushButton {background-color: #d4a373; color: white; border-radius: 5px; padding: 5px 10px;}"
            "QPushButton:hover {background-color: #bc6c25;}"
        )
        self.close_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        # 添加到主布局
        main_layout.addWidget(QLabel("历史占卜记录:"), alignment=Qt.AlignLeft)
        main_layout.addWidget(self.history_list)
        main_layout.addWidget(self.detail_group)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def on_history_item_clicked(self, item):
        index = item.data(Qt.UserRole)
        history_item = self.history[-(index + 1)]  # 反转索引，因为列表是反向显示的
        
        self.question_content.setText(history_item['question'])
        
        cards_text = "\n".join([f"{card['name']} ({card['orientation']}) - {card['meaning']}" for card in history_item['cards']])
        self.cards_content.setText(cards_text)
        
        self.analysis_content.setText(history_item['analysis'])
    
    def delete_history_item(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择要删除的记录")
            return
        
        for item in selected_items:
            index = item.data(Qt.UserRole)
            del self.history[-(index + 1)]  # 删除对应的历史记录
            
        # 刷新列表
        self.history_list.clear()
        for i, item in enumerate(reversed(self.history)):
            list_item = QListWidgetItem(f"{item['timestamp']} - {item['question'][:30]}...")
            list_item.setData(Qt.UserRole, i)
            self.history_list.addItem(list_item)
        
        # 清空详情
        self.question_content.setText("")
        self.cards_content.setText("")
        self.analysis_content.setText("")
        
    def copy_history_info(self):
        selected_items = self.history_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择要复制的记录")
            return
        
        item = selected_items[0]
        index = item.data(Qt.UserRole)
        history_item = self.history[-(index + 1)]  # 反转索引，因为列表是反向显示的
        
        # 收集信息
        cards_info = [f"问题：{history_item['question']}。"]
        for i, card in enumerate(history_item['cards'], 1):
            cards_info.append(f"第{i}张：{card['name']} ({card['orientation']})")
        
        # 拼接成文本
        cards_text = "\n".join(cards_info)
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)
        
        
    def closeEvent(self, event):
        # 保存历史记录
        self.parent().save_history()
        event.accept()

class AIAnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #f8f0e5;
            border-radius: 10px;
            border: 2px solid #d4a373;
            padding: 15px;
        """)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("AI 智慧解读")
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #432818;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # 分析内容
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setFont(QFont("Arial", 10))
        self.analysis_text.setStyleSheet("""
            background-color: #f9f5f0;
            border: 1px solid #d4a373;
            border-radius: 5px;
            padding: 10px;
            color: #432818;
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(self.analysis_text)
        
        self.setLayout(layout)
        self.worker = None
    
    def set_analysis(self, question, cards, callback=None):
        # 显示加载状态
        self.analysis_text.setText("正在生成AI解读，请稍候...")

        # 存储回调
        self.callback = callback

        # 如果已有worker在运行，先停止
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        # 创建并启动新的worker线程
        self.worker = AIAnalysisWorker(question, cards)
        self.worker.analysis_update.connect(self.on_analysis_update)
        self.worker.analysis_complete.connect(self.on_analysis_complete)
        self.worker.analysis_error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_update(self, partial_text):
        """实时更新AI解读文本"""
        self.analysis_text.setText(partial_text)
        # 滚动到底部，便于查看最新输出
        self.analysis_text.verticalScrollBar().setValue(self.analysis_text.verticalScrollBar().maximum())

    def on_analysis_complete(self, analysis):
        self.analysis_text.setText(analysis)
        # 调用回调
        if hasattr(self, 'callback') and self.callback:
            self.callback(analysis, None)

    def on_analysis_error(self, error_message):
        self.analysis_text.setText(error_message)
        # 错误情况下也调用回调，但传递None
        if hasattr(self, 'callback') and self.callback:
            self.callback(None, error_message)

class TarotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 塔罗牌占卜")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #f9f5f0;")
        
        # 设置应用图标
        self.setWindowIcon(QIcon("tarot_icon.png"))  # 需要准备图标文件
        
        # 初始化UI
        self.init_ui()
        
        # 创建牌堆
        self.deck = TarotDeck()
        
        # 存储当前抽到的牌
        self.drawn_cards = []
        
        # 历史记录
        self.history = []
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tarot_history.json')
        self.load_history()
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {str(e)}")
            self.history = []
    
    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {str(e)}")
    
    def show_history(self):
        """显示历史记录对话框"""
        history_dialog = HistoryDialog(self.history, self)
        history_dialog.exec_()
    
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("AI 塔罗牌占卜")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #432818;")
        title_label.setAlignment(Qt.AlignCenter)
        
        # 副标题
        subtitle_label = QLabel("输入您的问题，让塔罗牌揭示隐藏的智慧")
        subtitle_font = QFont("Arial", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6c584c;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        # 问题输入区域
        question_group = QGroupBox("您的问题")
        question_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #432818;
                border: 2px solid #d4a373;
                border-radius: 10px;
                margin-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        question_layout = QVBoxLayout()
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入您想询问的问题...")
        self.question_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8f0e5;
                border: 1px solid #d4a373;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                color: #432818;
            }
        """)
        self.question_input.setMinimumHeight(40)
        
        question_layout.addWidget(self.question_input)
        question_group.setLayout(question_layout)
        
        # 控制区域
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # 历史记录按钮
        self.history_button = QPushButton("历史记录")
        self.history_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.history_button.setStyleSheet("""
            QPushButton {
                background-color: #d4a373;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bc6c25;
            }
        """)
        self.history_button.clicked.connect(self.show_history)
        self.history_button.setCursor(Qt.PointingHandCursor)
        
        # 复制按钮
        self.copy_button = QPushButton("复制牌面")
        self.copy_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #d4a373;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bc6c25;
            }
        """)
        self.copy_button.clicked.connect(self.copy_cards_info)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setEnabled(False)  # 初始时禁用，抽牌后启用
        
        # 抽牌数量选择
        count_layout = QHBoxLayout()
        count_label = QLabel("抽牌数量:")
        count_label.setFont(QFont("Arial", 12))
        count_label.setStyleSheet("color: #432818;")
        
        self.card_count = QComboBox()
        self.card_count.setStyleSheet("""
            QComboBox {
                background-color: #f8f0e5;
                border: 1px solid #d4a373;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #432818;
            }
            QComboBox::drop-down {
                border-left: 1px solid #d4a373;
            }
        """)
        
        # 添加选项和工具提示
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
        
        self.card_count.setCurrentIndex(1)  # 默认选择3张牌
        
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.card_count)
        count_layout.addStretch()
        
        # 抽牌按钮
        self.draw_button = QPushButton("抽取塔罗牌")
        self.draw_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.draw_button.setStyleSheet("""
            QPushButton {
                background-color: #d4a373;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bc6c25;
            }
        """)
        self.draw_button.clicked.connect(self.draw_cards)
        self.draw_button.setCursor(Qt.PointingHandCursor)
        
        control_layout.addWidget(self.history_button)
        control_layout.addWidget(self.copy_button)
        control_layout.addLayout(count_layout)
        control_layout.addWidget(self.draw_button)
        
        # 卡片显示区域
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.cards_layout.setSpacing(20)
        self.cards_container.setLayout(self.cards_layout)
        self.cards_scroll.setWidget(self.cards_container)
        
        # AI分析区域
        self.analysis_widget = AIAnalysisWidget()
        
        # 添加到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(question_group)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(QLabel("抽取的塔罗牌:"), alignment=Qt.AlignLeft)
        main_layout.addWidget(self.cards_scroll)
        main_layout.addWidget(self.analysis_widget)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def copy_cards_info(self):
        # 获取问题
        question = self.question_input.text().strip()
        
        # 收集所有牌的信息
        cards_info = [f"问题：{question}。"]
        for i, card in enumerate(self.drawn_cards, 1):
            cards_info.append(f"第{i}张：{card.name} ({card.orientation})")
        
        # 拼接成文本
        cards_text = "\n".join(cards_info)
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(cards_text)
        
        
    def draw_cards(self):
        # 获取问题
        question = self.question_input.text().strip()
        if not question:
            self.question_input.setPlaceholderText("请先输入您的问题...")
            return
        
        # 获取抽牌数量
        num_cards = int(self.card_count.currentText())
        
        # 清空之前的卡片
        for i in reversed(range(self.cards_layout.count())): 
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        # 洗牌并抽牌
        self.deck = TarotDeck()  # 创建新牌堆
        self.drawn_cards = self.deck.draw(num_cards)
        
        # 显示抽到的牌
        for card in self.drawn_cards:
            card_widget = CardWidget(card)
            self.cards_layout.addWidget(card_widget)
        
        # 启用复制按钮
        self.copy_button.setEnabled(True)
        
        # 定义回调函数，用于保存历史记录
        def save_history_callback(analysis, error):
            if analysis and not error:
                # 创建历史记录项
                history_item = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'question': question,
                    'cards': [{
                        'name': card.name,
                        'orientation': card.orientation,
                        'meaning': card.meaning,
                        'interpretation': card.get_interpretation()
                    } for card in self.drawn_cards],
                    'analysis': analysis
                }
                
                # 添加到历史记录
                self.history.append(history_item)
                
                # 保存历史记录
                self.save_history()
            
        # 生成AI分析，并传递回调函数
        self.analysis_widget.set_analysis(question, self.drawn_cards, save_history_callback)