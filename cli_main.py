import os
import sys
import json
import re
from datetime import datetime
from tarot_deck import TarotDeck
from ai_analysis import AIAnalysisWorker

# 用于在CLI中同步获取AI分析结果
from PyQt5.QtCore import QCoreApplication

# 尝试使用prompt_toolkit实现现代化CLI补全
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

# 尝试使用readline作为备选方案
try:
    import readline  # 用于命令补全
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

class CLITarotApp:
    def __init__(self):
        self.deck = TarotDeck()
        self.history = []
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tarot_history.json')
        self.load_history()
        
        # 创建QApplication实例以支持QThread
        self.app = QCoreApplication(sys.argv)
        
        # 初始化现代化CLI输入系统
        self.input_method = "basic"  # 默认为基本输入
        
        if PROMPT_TOOLKIT_AVAILABLE:
            try:
                from prompt_toolkit import PromptSession
                from prompt_toolkit.completion import WordCompleter
                from prompt_toolkit.history import FileHistory
                from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
                
                # 初始化prompt_toolkit会话
                self.session = PromptSession(
                    history=FileHistory(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.tarot_cli_history'))
                )
                
                # 设置命令补全器
                self.command_completer = WordCompleter(
                    ['/history', '/quit', '/exit', '/help'],
                    ignore_case=True,
                    sentence=True
                )
                
                # 设置数字补全器（用于抽牌数量）
                self.number_completer = WordCompleter(
                    ['1', '3', '5', '7', '10'],
                    ignore_case=True,
                    sentence=True
                )

                self.mode_completer = WordCompleter(
                    ['1', '2'],
                    ignore_case=True,
                    sentence=True
                )
                
                self.input_method = "prompt_toolkit"
            except Exception:
                # 如果prompt_toolkit初始化失败，回退到readline
                if READLINE_AVAILABLE:
                    self.setup_readline_completion()
                    self.input_method = "readline"
        elif READLINE_AVAILABLE:
            self.setup_readline_completion()
            self.input_method = "readline"
        
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
            
    def setup_readline_completion(self):
        """设置readline命令补全"""
        # 定义补全函数
        def completer(text, state):
            options = ['/history', '/quit', '/exit']
            matches = [option for option in options if option.startswith(text)]
            if state < len(matches):
                return matches[state]
            else:
                return None
                
        # 设置补全函数
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    def show_history(self):
        """显示历史记录"""
        if not self.history:
            print("暂无历史记录。")
            return
            
        print("\n=== 历史记录 ===")
        for i, item in enumerate(reversed(self.history[-10:]), 1):  # 显示最近10条
            print(f"{i}. {item['timestamp']} - {item['question'][:30]}...")
            
        choice = input("\n输入记录编号查看详情，或按回车返回: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.history[-10:]):
            index = len(self.history) - int(choice)
            self.show_history_detail(self.history[index])
        elif choice:
            print("无效选择。")

    def show_history_detail(self, history_item):
        """显示历史记录详情"""
        draw_mode = history_item.get('draw_mode', 'auto')
        draw_mode_text = '自选模式' if draw_mode == 'manual' else '自动模式'

        print(f"\n问题: {history_item['question']}")
        print(f"抽牌模式: {draw_mode_text}")
        print("\n抽取的牌:")
        for card in history_item['cards']:
            print(f"  {card['name']} ({card['orientation']}) - {card['meaning']}")
        print(f"\n解读结果:\n{history_item['analysis']}")
        input("\n按回车返回...")

    def parse_manual_indices(self, raw_text, expected_count, max_index):
        normalized_text = raw_text.replace('，', ',').strip()
        tokens = [item for item in re.split(r'[\s,]+', normalized_text) if item]

        if len(tokens) != expected_count:
            raise ValueError(f"请输入 {expected_count} 个序号")

        indices = []
        seen = set()

        for token in tokens:
            if not token.isdigit():
                raise ValueError("序号必须是数字")

            index = int(token)
            if index < 1 or index > max_index:
                raise ValueError(f"序号超出范围，请输入 1 到 {max_index} 之间的数字")
            if index in seen:
                raise ValueError("序号不能重复")

            seen.add(index)
            indices.append(index)

        return indices

    def copy_cards_info(self, question, drawn_cards):
        """复制牌面信息到剪贴板（CLI版本简化为打印）"""
        print("\n=== 牌面信息 ===")
        print(f"问题：{question}")
        for i, card in enumerate(drawn_cards, 1):
            print(f"第{i}张：{card.name} ({card.orientation})")
        print("================")

    def get_ai_analysis(self, question, cards):
        """获取AI分析结果"""
        print("\n正在生成AI解读，请稍候...")
        
        # 创建worker
        worker = AIAnalysisWorker(question, cards)
        
        # 用于存储结果
        analysis_result = [None]  # 使用列表以便在内部函数中修改
        error_occurred = [False]
        
        # 连接信号
        def on_update(partial_text):
            # 实时更新，CLI中我们不显示部分结果，但可以保留这个功能
            pass
            
        def on_complete(analysis):
            analysis_result[0] = analysis
            self.app.quit()  # 结束事件循环
            
        def on_error(error_message):
            analysis_result[0] = error_message
            error_occurred[0] = True
            self.app.quit()  # 结束事件循环
            
        worker.analysis_update.connect(on_update)
        worker.analysis_complete.connect(on_complete)
        worker.analysis_error.connect(on_error)
        
        # 启动worker
        worker.start()
        
        # 运行事件循环直到完成
        self.app.exec_()
        
        # 返回结果
        if error_occurred[0]:
            print(f"AI分析出错: {analysis_result[0]}")
            return None
        return analysis_result[0]

    def draw_cards(self, question, num_cards, draw_mode='auto'):
        """抽牌并进行解读"""
        # 洗牌并抽牌
        self.deck = TarotDeck()  # 创建新牌堆
        if draw_mode == 'manual':
            while True:
                try:
                    print(f"\n当前为自选模式，请在 1-{len(self.deck.cards)} 中选择 {num_cards} 个序号")
                    print("输入示例: 3 12 25 或 3,12,25")
                    manual_input = input("请输入牌序号: ").strip()

                    if manual_input.lower() in ['/quit', '/exit']:
                        print("感谢使用AI塔罗牌占卜！")
                        return

                    indices = self.parse_manual_indices(manual_input, num_cards, len(self.deck.cards))
                    drawn_cards = self.deck.draw_by_indices(indices)
                    break
                except ValueError as e:
                    print(f"输入无效: {str(e)}")
        else:
            drawn_cards = self.deck.draw(num_cards)
        
        # 显示抽到的牌
        print(f"\n问题: {question}")
        print("\n抽取的塔罗牌:")
        for i, card in enumerate(drawn_cards, 1):
            print(f"第{i}张: {card.name} ({card.orientation})")
            print(f"  基本含义: {card.meaning}")
            print(f"  具体解释: {card.get_interpretation()}")
            print()
        
        # 生成AI分析
        analysis = self.get_ai_analysis(question, drawn_cards)
        
        if analysis:
            print("AI解读结果:")
            print(analysis)
            
            # 保存到历史记录
            history_item = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'question': question,
                'draw_mode': draw_mode,
                'cards': [{
                    'name': card.name,
                    'orientation': card.orientation,
                    'meaning': card.meaning,
                    'interpretation': card.get_interpretation()
                } for card in drawn_cards],
                'analysis': analysis
            }
            
            self.history.append(history_item)
            self.save_history()
            
            # 询问是否复制牌面信息
            copy_choice = input("\n是否复制牌面信息? (y/n): ").strip().lower()
            if copy_choice == 'y':
                self.copy_cards_info(question, drawn_cards)

    def run(self):
        """运行CLI应用"""
        print("=== AI 塔罗牌占卜 (CLI版本) ===")
        print("输入 '/quit' 或 '/exit' 退出程序")
        print("输入 '/history' 查看历史记录")
        
        if self.input_method == "prompt_toolkit":
            print("使用 Tab 键可以补全命令")
            print("使用方向键可以浏览历史命令")
        elif self.input_method == "readline":
            print("使用 Tab 键可以补全命令")
        else:
            print("注意：当前系统不支持命令补全功能")
        
        while True:
            try:
                print("\n" + "="*50)
                
                # 根据可用的输入方法获取用户输入
                if self.input_method == "prompt_toolkit":
                    try:
                        command = self.session.prompt(
                            "请输入命令或问题: ",
                            completer=self.command_completer,
                            auto_suggest=AutoSuggestFromHistory()
                        ).strip()
                    except Exception:
                        # 如果prompt_toolkit出现问题，回退到基本输入
                        command = input("请输入命令或问题: ").strip()
                elif self.input_method == "readline":
                    command = input("请输入命令或问题: ").strip()
                else:
                    command = input("请输入命令或问题: ").strip()
                
                if command.lower() in ['/quit', '/exit']:
                    print("感谢使用AI塔罗牌占卜！")
                    break
                elif command.lower() == '/history':
                    self.show_history()
                    continue
                elif not command:
                    continue
                    
                # 询问抽牌数量
                while True:
                    try:
                        # 根据可用的输入方法获取抽牌数量
                        if self.input_method == "prompt_toolkit":
                            try:
                                num_cards_input = self.session.prompt(
                                    "请选择抽牌数量 (1/3/5/7/10): ",
                                    completer=self.number_completer,
                                    auto_suggest=AutoSuggestFromHistory()
                                ).strip()
                            except Exception:
                                # 如果prompt_toolkit出现问题，回退到基本输入
                                num_cards_input = input("请选择抽牌数量 (1/3/5/7/10): ").strip()
                        else:
                            num_cards_input = input("请选择抽牌数量 (1/3/5/7/10): ").strip()
                            
                        if num_cards_input.lower() in ['/quit', '/exit']:
                            print("感谢使用AI塔罗牌占卜！")
                            return
                        num_cards = int(num_cards_input)
                        if num_cards in [1, 3, 5, 7, 10]:
                            break
                        else:
                            print("请输入有效的抽牌数量: 1, 3, 5, 7, 或 10")
                    except ValueError:
                        print("请输入有效的数字")

                # 选择抽牌模式
                while True:
                    if self.input_method == "prompt_toolkit":
                        try:
                            mode_input = self.session.prompt(
                                "请选择抽牌模式 (1=自动模式, 2=自选模式): ",
                                completer=self.mode_completer,
                                auto_suggest=AutoSuggestFromHistory()
                            ).strip()
                        except Exception:
                            mode_input = input("请选择抽牌模式 (1=自动模式, 2=自选模式): ").strip()
                    else:
                        mode_input = input("请选择抽牌模式 (1=自动模式, 2=自选模式): ").strip()

                    if mode_input.lower() in ['/quit', '/exit']:
                        print("感谢使用AI塔罗牌占卜！")
                        return

                    if mode_input == '1':
                        draw_mode = 'auto'
                        break
                    if mode_input == '2':
                        draw_mode = 'manual'
                        break

                    print("请输入 1 或 2")
                        
                # 抽牌并解读
                self.draw_cards(command, num_cards, draw_mode)
                
            except (EOFError, KeyboardInterrupt):
                # 处理 Ctrl+C 或 Ctrl+D
                print("\n\n感谢使用AI塔罗牌占卜！")
                break

def main():
    app = CLITarotApp()
    app.run()

if __name__ == '__main__':
    main()
