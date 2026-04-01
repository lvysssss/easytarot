"""
GUI组件包入口
导出所有组件类
"""

from gui.widgets.title_bar import DraggableTitleBar
from gui.widgets.card_widget import ModernCardWidget
from gui.widgets.history_dialog import ModernHistoryDialog
from gui.widgets.analysis_widget import ModernAIAnalysisWidget

__all__ = [
    "DraggableTitleBar",
    "ModernCardWidget",
    "ModernHistoryDialog",
    "ModernAIAnalysisWidget",
]