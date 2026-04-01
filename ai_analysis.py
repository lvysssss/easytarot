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

            prompt = self.build_prompt()

            partial_text = ""
            print(f"[DEBUG] 开始调用API，模型: {self.model_name}")
            
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
                    print(f"[DEBUG] Chunk {chunk_count}: 没有 choices")
                    continue
                
                delta = chunk.choices[0].delta
                if delta is None:
                    print(f"[DEBUG] Chunk {chunk_count}: delta 为 None")
                    continue
                
                content = getattr(delta, 'content', None)
                if content:
                    partial_text += content
                    print(f"[DEBUG] Chunk {chunk_count}: 收到内容长度={len(content)}, 累计长度={len(partial_text)}")
                    self.analysis_update.emit(partial_text)
                else:
                    print(f"[DEBUG] Chunk {chunk_count}: content 为空或 None")

            print(f"[DEBUG] 流式响应结束，共 {chunk_count} 个 chunk，最终文本长度: {len(partial_text)}")
            
            if partial_text.strip():
                self.analysis_complete.emit(partial_text.strip())
            else:
                self.analysis_error.emit("AI返回了空内容，请检查API配置或模型是否可用")
                
        except Exception as e:
            print(f"[DEBUG] 异常: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
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
        prompt += "要求:1.语言要通俗易懂，避免过于专业的术语\n"

        return prompt