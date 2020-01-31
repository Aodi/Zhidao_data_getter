from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
"""
按钮ID说明：  

comboBox: 复选框
lineEdit: 输入关键字的输入框
Button1： 检索数据  按钮
Button2: 预览数据  按钮
Button3：获取数据  按钮  
Output:  输出窗口  
ClearButton：清除内容按钮

"""
class Stats:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('PaCApp.ui')

        self.ui.comboBox.addItems(['百度知道', '专家在线'])

    # def prt(self):
    #     print("点击了‘检索数据’按钮！")

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()