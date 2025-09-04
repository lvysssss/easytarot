import sys
import argparse
from PyQt5.QtWidgets import QApplication
from gui import TarotApp
from cli_main import main as cli_main


def main():
    parser = argparse.ArgumentParser(description='AI 塔罗牌占卜程序')
    parser.add_argument('--cli', action='store_true', help='使用命令行界面 (CLI) 模式')
    
    args = parser.parse_args()
    
    if args.cli:
        # 运行CLI版本
        cli_main()
    else:
        # 创建应用程序实例
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle('Fusion')
        
        # 创建主窗口
        window = TarotApp()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()