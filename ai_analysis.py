import os
from dotenv import load_dotenv
from openai import OpenAI
from PyQt5.QtCore import QThread, pyqtSignal

class AIAnalysisWorker(QThread):
    analysis_update = pyqtSignal(str)  # 实时部分文本
    analysis_complete = pyqtSignal(str)
    analysis_error = pyqtSignal(str)

    def __init__(self, question, cards):
        super().__init__()
        self.question = question
        self.cards = cards
        self.client = None

        # 从环境变量或配置文件加载OpenAI API密钥并创建客户端
        self.load_api_key()

    def load_api_key(self):
        """加载OpenAI API密钥并创建客户端"""
        try:
            for key in ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL_NAME']:
                if key in os.environ:
                    del os.environ[key]
            
            load_dotenv(override=True)
            
            api_key = os.environ.get('OPENAI_API_KEY')
            base_url = os.environ.get('OPENAI_BASE_URL')
            
            if api_key:
                client_kwargs = {'api_key': api_key}
                if base_url:
                    client_kwargs['base_url'] = base_url.rstrip('/')
                self.client = OpenAI(**client_kwargs)
                self.model_name = os.environ.get('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
            else:
                raise Exception("未找到OpenAI API密钥，请在.env文件中设置OPENAI_API_KEY")
        except Exception as e:
            self.analysis_error.emit(f"加载API密钥失败: {str(e)}")

    def run(self):
        """运行AI分析（流式输出）"""
        try:
            if not self.client:
                self.analysis_error.emit("未初始化OpenAI客户端")
                return

            # 构建提示词
            prompt = self.build_prompt()

            # 以流式方式调用 OpenAI 接口
            partial_text = ""
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一位专业的塔罗牌解读师，拥有丰富的塔罗牌知识和解读经验。你能够根据用户的问题和抽取的塔罗牌，提供深入、准确且有洞察力的解读。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10000,
                temperature=0.7,
                stream=True
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    partial_text += delta.content
                    self.analysis_update.emit(partial_text)

            # 发送完成信号
            self.analysis_complete.emit(partial_text.strip())
        except Exception as e:
            self.analysis_error.emit(f"AI分析失败: {str(e)}")

    def build_prompt(self):
        """构建提示词"""
        prompt = f"用户的问题: {self.question}\n\n"
        prompt += "抽取的塔罗牌:\n"

        for i, card in enumerate(self.cards, 1):
            prompt += f"第{i}张牌: {card.name} ({card.orientation})\n"
            prompt += f"基本含义: {card.meaning}\n"
            prompt += f"具体解释: {card.get_interpretation()}\n\n"

        prompt += "请根据用户的问题和抽取的塔罗牌，提供一个深入、准确且有洞察力的解读。解读应包括:\n"
        prompt += "1. 对每张牌在问题背景下的含义解读\n"
        prompt += "2. 牌与牌之间的关联分析\n"
        prompt += "3. 针对用户问题的整体建议\n"
        prompt += "4. 语言要通俗易懂，避免过于专业的术语\n"
        prompt += "5. 保持积极正面的态度，给予用户鼓励和支持"

        return prompt