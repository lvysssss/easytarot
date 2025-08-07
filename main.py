import sys
from PyQt5.QtWidgets import QApplication
from gui import TarotApp

def main():
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