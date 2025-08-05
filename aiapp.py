import sys
import random
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import openai
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QSpinBox, QTextEdit, QFrame, QComboBox,
                             QScrollArea, QGroupBox, QListWidget, QListWidgetItem, QDialog, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPalette, QClipboard
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from openai import OpenAI

# 加载.env文件中的配置
load_dotenv()

# 从环境变量中获取API配置
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

# 配置OpenAI客户端
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class TarotCard:
    def __init__(self, name, meaning, upright, reversed_meaning, suit=None, arcana="Major"):
        self.name = name
        self.meaning = meaning
        self.upright = upright
        self.reversed_meaning = reversed_meaning
        self.suit = suit
        self.arcana = arcana
        self.orientation = "正位" if random.random() > 0.5 else "逆位"
    
    def get_interpretation(self):
        if self.orientation == "正位":
            return self.upright
        return self.reversed_meaning
    
    def __str__(self):
        return f"{self.name} ({self.orientation})"

class TarotDeck:
    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()
    
    def create_deck(self):
        cards = []
        
        # 大阿卡纳牌
        major_arcana = [
            ("愚者", "新的开始、冒险", "新的旅程开始，充满潜力", "鲁莽、冒险失败", "Major"),
            ("魔术师", "创造力、意志力", "运用技能实现目标", "欺骗、操纵", "Major"),
            ("女祭司", "直觉、潜意识", "倾听直觉，内在智慧", "忽视直觉，压抑情感", "Major"),
            ("皇后", "丰饶、母性", "创造力，丰盛富足", "依赖，过度保护", "Major"),
            ("皇帝", "权威、结构", "领导力，建立秩序", "控制欲强，僵化", "Major"),
            ("教皇", "传统、精神指导", "寻求智慧，精神指引", "教条主义，盲从", "Major"),
            ("恋人", "爱情、选择", "和谐关系，重要选择", "不和谐，错误选择", "Major"),
            ("战车", "意志力、胜利", "克服障碍，取得成功", "失去方向，冲突", "Major"),
            ("力量", "勇气、耐心", "内在力量，克服挑战", "自我怀疑，无力感", "Major"),
            ("隐士", "内省、寻求真理", "自我反思，寻找答案", "孤独，逃避现实", "Major"),
            ("命运之轮", "命运、转折点", "积极变化，命运转折", "消极变化，抗拒改变", "Major"),
            ("正义", "公正、真理", "公平决定，承担责任", "不公正，逃避责任", "Major"),
            ("倒吊人", "牺牲、新视角", "换位思考，接受现状", "拖延，无谓牺牲", "Major"),
            ("死神", "结束、转变", "结束与新生，转变", "抗拒改变，停滞不前", "Major"),
            ("节制", "平衡、调和", "平衡和谐，自我控制", "失衡，极端行为", "Major"),
            ("恶魔", "束缚、物质主义", "物质束缚，欲望控制", "摆脱束缚，精神解放", "Major"),
            ("塔", "剧变、启示", "重大变化，突破束缚", "避免灾难，小挫折", "Major"),
            ("星星", "希望、灵感", "希望重生，精神觉醒", "失去希望，悲观", "Major"),
            ("月亮", "幻觉、潜意识", "面对恐惧，探索潜意识", "困惑，自我欺骗", "Major"),
            ("太阳", "快乐、成功", "成功快乐，积极能量", "暂时挫折，小成功", "Major"),
            ("审判", "重生、内在召唤", "自我觉醒，新的开始", "自我怀疑，错失机会", "Major"),
            ("世界", "完成、成就", "圆满成功，成就达成", "未完成，需要努力", "Major")
        ]
        
        for name, meaning, upright, reversed_meaning, arcana in major_arcana:
            cards.append(TarotCard(name, meaning, upright, reversed_meaning, arcana=arcana))
        
        # 小阿卡纳牌 - 权杖
        wands = [
            ("权杖一", "新行动、创造力", "新计划开始，充满能量", "延迟，缺乏方向", "权杖"),
            ("权杖二", "规划、决策", "未来规划，做出决定", "恐惧改变，犹豫不决", "权杖"),
            ("权杖三", "远见、合作", "展望未来，团队合作", "缺乏远见，独自奋斗", "权杖"),
            ("权杖四", "庆祝、稳定", "庆祝成就，稳定和谐", "不稳定，小问题", "权杖"),
            ("权杖五", "冲突、竞争", "健康竞争，解决冲突", "避免冲突，内部斗争", "权杖"),
            ("权杖六", "胜利、认可", "获得认可，成功在望", "挫折，缺乏认可", "权杖"),
            ("权杖七", "挑战、坚持", "面对挑战，坚持立场", "不堪重负，放弃", "权杖"),
            ("权杖八", "快速行动、进展", "快速进展，消息传来", "延迟，计划混乱", "权杖"),
            ("权杖九", "毅力、警惕", "坚持到底，保持警惕", "偏执，过度防御", "权杖"),
            ("权杖十", "负担、责任", "责任过重，需要帮助", "放下负担，委派任务", "权杖"),
        ]
        
        # 小阿卡纳牌 - 圣杯
        cups = [
            ("圣杯一", "新情感、直觉", "新情感开始，直觉增强", "情感空虚，直觉受阻", "圣杯"),
            ("圣杯二", "和谐、伙伴关系", "和谐关系，平等合作", "不平衡，沟通问题", "圣杯"),
            ("圣杯三", "庆祝、友谊", "庆祝成就，朋友相聚", "过度享乐，表面关系", "圣杯"),
            ("圣杯四", "沉思、不满", "自我反思，评估选择", "错失机会，过度消极", "圣杯"),
            ("圣杯五", "失落、悲伤", "接受失落，寻找希望", "沉溺悲伤，忽视积极", "圣杯"),
            ("圣杯六", "回忆、童年", "美好回忆，怀旧之情", "活在回忆，逃避现实", "圣杯"),
            ("圣杯七", "选择、幻想", "明确目标，做出选择", "困惑，不切实际", "圣杯"),
            ("圣杯八", "离开、寻找", "寻求更深意义，离开舒适区", "恐惧改变，安于现状", "圣杯"),
            ("圣杯九", "满足、愿望成真", "愿望实现，自我满足", "物质满足，精神空虚", "圣杯"),
            ("圣杯十", "和谐、家庭", "家庭和谐，情感满足", "家庭冲突，不和谐", "圣杯"),
        ]
        
        # 小阿卡纳牌 - 宝剑
        swords = [
            ("宝剑一", "新想法、突破", "思想清晰，突破困境", "混乱想法，负面思维", "宝剑"),
            ("宝剑二", "僵局、逃避", "做出决定，面对现实", "逃避现实，拒绝选择", "宝剑"),
            ("宝剑三", "心痛、悲伤", "接受痛苦，开始疗愈", "深陷痛苦，无法释怀", "宝剑"),
            ("宝剑四", "休息、恢复", "充分休息，恢复能量", "过度休息，逃避问题", "宝剑"),
            ("宝剑五", "冲突、胜利", "短期胜利，吸取教训", "不惜代价取胜，后悔", "宝剑"),
            ("宝剑六", "过渡、疗愈", "逐渐恢复，向前迈进", "停滞不前，无法释怀", "宝剑"),
            ("宝剑七", "欺骗、策略", "巧妙策略，避免冲突", "欺骗，不诚实行为", "宝剑"),
            ("宝剑八", "限制、无助", "发现出路，重获自由", "感觉被困，自我设限", "宝剑"),
            ("宝剑九", "焦虑、恐惧", "面对恐惧，寻求帮助", "过度焦虑，噩梦困扰", "宝剑"),
            ("宝剑十", "结束、新生", "困难结束，新的开始", "暂时挫折，需要坚持", "宝剑"),
        ]
        
        # 小阿卡纳牌 - 星币
        pentacles = [
            ("星币一", "新机会、财富", "新机会出现，财务稳定", "错失机会，财务不稳", "星币"),
            ("星币二", "平衡、适应", "灵活适应，平衡生活", "失衡，财务压力", "星币"),
            ("星币三", "团队合作、技能", "团队合作，技能发展", "缺乏合作，技能不足", "星币"),
            ("星币四", "保守、控制", "财务稳定，保护资源", "过度控制，吝啬", "星币"),
            ("星币五", "困难、贫困", "互相支持，共度难关", "孤立无援，财务危机", "星币"),
            ("星币六", "慷慨、分享", "慷慨分享，公平交易", "自私，不公平交易", "星币"),
            ("星币七", "评估、耐心", "评估进展，耐心等待", "缺乏耐心，投资失误", "星币"),
            ("星币八", "技艺、专注", "专注工作，技能提升", "缺乏动力，工作马虎", "星币"),
            ("星币九", "独立、享受", "享受成果，独立自主", "过度独立，物质主义", "星币"),
            ("星币十", "财富、家庭", "家庭富足，财务安全", "家庭冲突，财务问题", "星币"),
        ]
        
        # 添加小阿卡纳牌
        for suit_cards, suit_name in zip([wands, cups, swords, pentacles], ["权杖", "圣杯", "宝剑", "星币"]):
            for name, meaning, upright, reversed_meaning, _ in suit_cards:
                cards.append(TarotCard(name, meaning, upright, reversed_meaning, suit=suit_name, arcana="Minor"))
        
        return cards
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self, num_cards):
        if num_cards > len(self.cards):
            num_cards = len(self.cards)
        return [self.cards.pop() for _ in range(num_cards)]

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
        self.delete_button.setStyleSheet(""
            "QPushButton {background-color: #d4a373; color: white; border-radius: 5px; padding: 5px 10px;}"
            "QPushButton:hover {background-color: #bc6c25;}"
        )
        self.delete_button.clicked.connect(self.delete_history_item)
        
        self.close_button = QPushButton("关闭")
        self.close_button.setStyleSheet(""
            "QPushButton {background-color: #d4a373; color: white; border-radius: 5px; padding: 5px 10px;}"
            "QPushButton:hover {background-color: #bc6c25;}"
        )
        self.close_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.delete_button)
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
    
    def closeEvent(self, event):
        # 保存历史记录
        self.parent().save_history()
        event.accept()


class AIAnalysisWorker(QThread):
    analysis_complete = pyqtSignal(str)
    analysis_error = pyqtSignal(str)

    def __init__(self, question, cards):
        super().__init__()
        self.question = question
        self.cards = cards

    def run(self):
        try:
            # 准备发送给OpenAI的提示
            prompt = f"用户的问题: {self.question}\n\n"
            prompt += f"用户抽取了 {len(self.cards)} 张塔罗牌，以下是牌的信息:\n\n"

            # 添加每张牌的信息
            for i, card in enumerate(self.cards, 1):
                prompt += f"第 {i} 张牌: {card.name} ({card.orientation})\n"
                prompt += f"含义: {card.meaning}\n"
                prompt += f"详细解读: {card.get_interpretation()}\n\n"

            prompt += "请根据以上信息，为用户提供一个全面、深入的塔罗牌解读。解读应包括:\n"
            prompt += "1. 对每张牌的解释\n"
            prompt += "2. 整体的综合分析\n"
            prompt += "3. 针对用户问题的建议\n"
            prompt += "4. 鼓励用户的话语\n"
            prompt += "请用温暖、智慧的语气进行解读。"

            # 调用OpenAI API
            response = client.chat.completions.create(
                model=OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "## Role: 塔罗占卜师\n  - description: 资深的专业的塔罗牌占卜师，熟知各类牌阵和塔罗牌本身代表的含义，根据用户的[问题]、抽到的[牌阵]，给出牌阵占卜解析，解析结果包括[牌面解读、占卜结果、建议、谶语]。\n## Goals :\n  1. 为用户进行占卜\n  2. 当抽到的牌中出现一些对用户有较大影响的情况时，进行详细解读\n  3. 解答用户的追问\n## Skills1: 在对所抽取的牌阵进行解读、占卜、建议、生成谶语时，你具备以下技能：\n  1. 占卜系统知识: 熟悉78张塔罗牌的意义，以及各种牌阵的设计和使用。\n  2. 解读和分析技巧: 擅长从占卜结果中提取关键信息，分析各种可能性，并结合客户的具体情况进行解读。\n  3. 沟通技巧: 善于和客户建立良好的关系，通过有效的沟通来理解客户的问题和需求，并将占卜结果以易于理解的方式传达给客户。\n  4. 伦理知识和技能: 遵守一定的伦理原则，如保护客户的隐私，不进行无理的预测，以及尊重客户的自由意志和选择。\n## Skills2:在牌面解读方面，你具备以下技能：\n  1. 牌面解释技能：深入理解每张塔罗牌的基础含义。\n  2. 逆位解读能力：理解每张牌的正位、逆位含义。\n  3. 牌组关系理解能力：深知塔罗牌的意义可能会根据它们在牌阵中与其他牌的相对位置和关系而改变。\n  4. 牌组相互影响分析能力：擅长理解和分析牌阵中的牌如何相互作用和影响。\n  5. 牌阵布置知识：理解解和熟悉各种不同的牌阵布置，以及它们各自的含义和适用场合。\n  6. 直觉引导能力：可以凭借直觉去理解和解释牌阵。\n  7. 元素和符号理解能力：塔罗牌上的每一个元素和符号都有其特定的含义，能够理解和解读这些元素和符号。\n## Constrains :\n  1. 输出的语言要优雅古典柔和，带有一些神秘气息；\n  2. 必须对牌面的画面元素进行一些解释（基于伟特牌）；\n  3. 在解读中代入每一张牌的顺序在牌阵本身中设定的含义；\n  4. 避免描述自己的语气和语言风格，保持优雅和神秘感；\n  5. 在给出占卜结果时，避免给出过多\"心灵鸡汤\"；\n  6. 非常自信的给出预测和建议；\n  7. 严格按照指定格式输出内容。\n## OutputFormat :\n**牌面解读**\n[*牌阵位置1~n*]：[牌面信息]：[牌面解读]；\n**占卜结果**\n[占卜结果正文]\n**建议**\n[建议正文]\n**谶语**\n[谶语正文]\n\'\'\'\n\n特别注意：在最后，你一定要给出二维绝对的答案，是对还是错，适合还是不适合。"},
                    {"role": "user", "content": prompt}
                ]
            )

            # 提取回复内容
            analysis = response.choices[0].message.content
            self.analysis_complete.emit(analysis)

        except Exception as e:
            self.analysis_error.emit(f"AI分析过程中出错: {str(e)}\n\n请检查您的OpenAI API配置是否正确。")


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
        self.worker.analysis_complete.connect(self.on_analysis_complete)
        self.worker.analysis_error.connect(self.on_analysis_error)
        self.worker.start()

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
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
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
        # 收集所有牌的信息
        cards_info = []
        for i, card in enumerate(self.drawn_cards, 1):
            cards_info.append(f"第{i}张牌: {card.name} ({card.orientation})")
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(249, 245, 240))
    palette.setColor(QPalette.WindowText, QColor(67, 40, 24))
    app.setPalette(palette)
    
    window = TarotApp()
    window.show()
    sys.exit(app.exec_())
