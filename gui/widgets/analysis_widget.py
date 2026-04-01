"""
AI分析结果展示组件
显示AI解读的实时流式输出结果
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ai_analysis import AIAnalysisWorker


class ModernAIAnalysisWidget(QWidget):
    """AI分析结果展示组件"""

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
        """启动AI分析"""
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
        """实时更新分析文本"""
        self.analysis_text.setText(partial_text)
        self.analysis_text.verticalScrollBar().setValue(
            self.analysis_text.verticalScrollBar().maximum()
        )

    def on_analysis_complete(self, analysis):
        """分析完成"""
        self.analysis_text.setText(analysis)
        if hasattr(self, "callback") and self.callback:
            self.callback(analysis, None)

    def on_analysis_error(self, error_message):
        """分析出错"""
        self.analysis_text.setText(f"错误: {error_message}")
        if hasattr(self, "callback") and self.callback:
            self.callback(None, error_message)