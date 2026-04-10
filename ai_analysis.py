import os
import sys
import threading
from dotenv import load_dotenv
from openai import OpenAI


class AIAnalysisWorker:
    """AI分析工作器 - CLI版本（使用标准线程）"""

    def __init__(self, question, cards):
        self.question = question
        self.cards = cards
        self.client = None
        self.on_update = None  # 回调函数: on_update(text)
        self.on_complete = None  # 回调函数: on_complete(text)
        self.on_error = None  # 回调函数: on_error(text)

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
            if self.on_error:
                self.on_error(f"加载API密钥失败: {str(e)}")

    def start(self):
        """启动AI分析（在新线程中运行）"""
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        return thread

    def run(self):
        """运行AI分析（流式输出）"""
        try:
            if not self.client:
                if self.on_error:
                    self.on_error("未初始化OpenAI客户端")
                return

            prompt = self.build_prompt()

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

            chunk_count = 0
            for chunk in response:
                chunk_count += 1
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                if delta is None:
                    continue

                content = getattr(delta, 'content', None)
                if content:
                    partial_text += content
                    if self.on_update:
                        self.on_update(partial_text)

            if partial_text.strip():
                if self.on_complete:
                    self.on_complete(partial_text.strip())
            else:
                if self.on_error:
                    self.on_error("AI返回了空内容，请检查API配置或模型是否可用")

        except Exception as e:
            if self.on_error:
                self.on_error(f"AI分析失败: {str(e)}")

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
        prompt += "要求:1.语言要通俗易懂，避免过于专业的术语\n"
        prompt += "2.面对选项问题，尽可以给出最好的选项\n"
        return prompt
