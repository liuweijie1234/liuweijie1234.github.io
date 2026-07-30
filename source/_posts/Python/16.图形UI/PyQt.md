---
title: Python3 PyQt6
date: 2022-09-26 16:00:00
tags:
- Python
categories:
- Python
---




### 安装

```bash
pip install PyQt6
```

### 模块

PyQt6 类是由一系列模块组成的，包括如下的模块：

QtCore 模块是非 GUI 的核心库。这个模块用来处理时间、文件、目录、各种类型的数据、流（stream）、URLs，mime 类型、线程和进程。
QtGui 有窗口系统集成、事件处理、2D图形，基本图像、字体、文本的类。
QtWidgets 有创建经典风格的用户界面的类。
QtDBus 是使用 D-Bus 处理 IPC 通讯的类。
QtNetwork 是网络变成类，这些类使网络编程变得更容易，可移植性也更好，方便了 TCP/IP 和 UDP 服务端和客户端编程。
QtHelp 包含了创建、查看和搜索文档的类。
QtXml 包含了处理 XML 文件的类，实现了 SAX 和 DOM API。
QtSvg 提供了显示 SVG 的类，可缩放矢量图形(SVG)是一种描述二维图像和图像应用的 XML 语言。
QtSql 模块提供了数据库的类，
QtTest 提供了可以对 PyQt6 应用进行单元测试的工具。


[PyQt6解决ImportError: DLL load failed: 找不到指定的程序](https://blog.csdn.net/weixin_45458665/article/details/128291598)

### 界面模板

设计界面时，首先需要选择界面模板，主要分为三个类：

- Main Window
    from PyQt6.QtWidgets import QApplication, QMainWindow
- Widget
    from PyQt6.QtWidgets import QApplication, QWidget
- Dialog
    from PyQt6.QtWidgets import QApplication, QDialog

主要使用QMainWindow, 继承QWidget

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow


class Example(QMainWindow):

    def __init__(self):
        super().__init__()  # 调用父类 QMainWindow 的初始化函数，确保正确地初始化父类。
        self.initUI()  # 调用 initUI 方法，用于设置用户界面。

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))  # 设置工具提示的字体为 SansSerif，大小为 10。

        self.setToolTip('This is a <b>QMainWindow</b> widget')  # 设置主窗口的提示文本工具。
        self.statusBar().showMessage('Ready')  # 在窗口底部创建一个状态栏，并设置初始文本为 "Ready"。
        self.setGeometry(300, 300, 350, 250)  # 设置窗口的位置和大小，参数依次为窗口左上角的 x 坐标、y 坐标、宽度和高度。
        self.setWindowTitle('QMainWindow')  # 设置窗口标题
        self.show()  # 显示窗口


def main():
    app = QApplication(sys.argv)  # 创建一个应用程序对象
    ex = Example()  # 创建一个 Example 实例
    sys.exit(app.exec())  # 启动应用程序的事件循环，处理用户输入和其他事件，直到应用程序被关闭


if __name__ == '__main__':
    main()

```

### QMainWindow 常用的方法和属性

setCentralWidget(widget)：将一个 QWidget 对象设置为窗口的中央部件。

用例:
```python
central_widget = QWidget()  # QWidget() 可以是 QWidget() 的子类对象,比如 QLabel("Hello, World!")
self.setCentralWidget(central_widget)  # 居中
```


menuBar()：获取窗口的菜单栏。
用例:
```python
menu_bar = self.menuBar()
```

statusBar()：获取窗口的状态栏。
用例:
```python
status_bar = self.statusBar()

status_bar.showMessage('Ready')  # 在窗口底部创建一个状态栏，并设置初始文本为 "Ready"。

self.statusbar().show()  # 显示状态栏

self.statusbar().hide()  # 隐藏状态栏
```

addToolBar(toolBar)：添加一个工具栏，参数为一个 QToolBar 对象。
用例:
```python
tool_bar = QToolBar()
self.addToolBar(tool_bar)

# 示例
exitAct = QAction(QIcon('logout.png'), 'Exit', self)
exitAct.setShortcut('Ctrl+Q')
exitAct.triggered.connect(QApplication.instance().quit)

self.toolbar = self.addToolBar('Exit')
self.toolbar.addAction(exitAct)
```

setMenuBar(menuBar)：设置窗口的菜单栏，参数为一个 QMenuBar 对象。
用例:
```python
menu_bar = QMenuBar()
self.setMenuBar(menu_bar)
```

setStatusBar(statusBar)：设置窗口的状态栏，参数为一个 QStatusBar 对象。
用例:
```python
status_bar = QStatusBar()
self.setStatusBar(status_bar)
```
resize(350, 250): 设置窗口的大小
用例:
```python
self.resize(350, 250)
```
将窗口居中
```python
    self.resize(350, 250)
    self.center()

    def center(self):

        window_rect = self.frameGeometry()  # 获取窗口的几何形状
        center_point = self.screen().availableGeometry().center()  # 获取屏幕的中心点坐标
        # center_point = QApplication.primaryScreen().availableGeometry().center()

        window_rect.moveCenter(center_point)  # 将窗口的中心点移动到屏幕的中心点
        self.move(window_rect.topLeft())  # 窗口移动到计算后的新位置
```
self 指的是当前窗口对象，在 QMainWindow 中可使用此方式调用。
self.screen() / QApplication.primaryScreen() 返回当前窗口所在的屏幕对象。
availableGeometry() 返回该屏幕的可用区域，即去除了任务栏、面板等的屏幕区域。
center() 方法获取可用区域的中心点坐标。



setGeometry(300, 300, 350, 250): 设置窗口的位置和大小
用例:
```python
self.setGeometry(300, 300, 350, 250)  # 设置窗口的位置和大小，参数依次为窗口左上角的 x 坐标、y 坐标、宽度和高度。
```

setWindowTitle(title)：设置窗口的标题。
用例:
```python
self.setWindowTitle('My Window')
```

setWindowIcon(icon)：设置窗口的图标。
用例:
```python
icon = QIcon('icon.png')
self.setWindowIcon(icon)
```

setFixedSize(width, height)：设置窗口的固定大小，即禁止用户调整窗口大小。
用例:
```python
self.setFixedSize(800, 600)
```

setWindowFlags(flags)：设置窗口的标志，例如是否显示标题栏、关闭按钮等。
用例:
```python
self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
```

centralWidget()：获取窗口的中央部件。
用例:
```python
central_widget = self.centralWidget()
```

close()：关闭窗口。
用例:
```python
self.close()
```

showMaximized()：最大化窗口。
用例:
```python
self.showMaximized()
```

showMinimized()：最小化窗口。
用例:
```python
self.showMinimized()
```

showNormal()：将窗口还原到正常大小和位置。
用例:
```python
self.showNormal()
```



### 接口组件

下面这几篇文章，会介绍 PyQt6 里用来设计接口的组件以及相关用法。

#### QLabel 标签

```python
        lbl1 = QLabel('ZetCode', self)
        lbl1.move(15, 10)
```



#### QPushButton 按钮

```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolTip, QPushButton)
from PyQt6.QtGui import QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))  # 设置工具提示的字体为 SansSerif，大小为 10。
        
        btn = QPushButton('开始压测', self)  # 创建一个名为 开始压测 的按钮，并将其放置在主窗口中。
        btn.setToolTip('This is a <b>QPushButton</b> widget')  # 设置按钮的工具提示文本。
        btn.resize(btn.sizeHint())  # 调整按钮的大小以适应内容。
        btn.move(50, 50)  # 移动按钮的位置到坐标 (50, 50)。

        qbtn = QPushButton('退出', self)  # 创建一个名为 退出 的按钮，并将其放置在主窗口中。
        qbtn.clicked.connect(QApplication.instance().quit)  # 该行将点击信号连接到 QApplication 实例方法 quit() 上，以便在单击按钮时终止应用程序。
        qbtn.resize(qbtn.sizeHint())  # 该行调整按钮的大小以适应按钮文本的大小。sizeHint() 方法返回建议大小，即可包含按钮文本的最小矩形。
        qbtn.move(150, 50)  # 移动按钮的位置到坐标 (150, 50)。
```


QRadioButton 单选按钮
QCheckBox 复选按钮
QGraphicsView 显示图片

QLineEdit 单行输入框




QTextEdit、QPlainTextEdit 多行输入框
QListWidget 列表选择框

QComboBox 下拉菜单

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        combo_box = QComboBox(self)
        combo_box.addItem("Option 1")
        combo_box.addItem("Option 2")
        combo_box.addItem("Option 3")
        combo_box.addItem("Option 4")

        combo_box.move(50, 50)
        combo_box.currentIndexChanged.connect(self.onComboBoxChanged)

        self.setWindowTitle("Dropdown Button")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onComboBoxChanged(self, index):
        selected_option = self.sender().currentText()
        print(f"Selected option: {selected_option}")

app = QApplication([])
window = MyWindow()
app.exec()

```


QSpinBox、QDoubleSpinBox 数值调整组件
QTimeEdit 时间调整元件
QDateEdit 日期调整元件
QSlider 数值调整滑杆
QProgressBar 进度条

### 窗口组件

下面这几篇文章，会介绍 PyQt6 里用来设计跟主要接口比较无关的元件。

#### QMenuBar、QMenu、QAction 窗口菜单

```python

from PyQt6.QtGui import QIcon, QAction

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAct = QAction(QIcon('exit.png'), '&退出', self)  # 创建一个 QAction 对象，并指定了该动作的图标、文本和父对象。
        exitAct.setShortcut('Ctrl+Q')  # 设置动作的快捷键为 "Ctrl+Q"。
        exitAct.setStatusTip('退出应用')  # 设置动作的状态提示信息为 "退出应用"，当鼠标悬停在该动作上时会显示该信息。
        exitAct.triggered.connect(QApplication.instance().quit)  # 当用户选择该动作时，将触发 QApplication.instance().quit 方法，即退出应用程序。

        self.statusBar()  # 创建一个状态栏对象，并将其添加到主窗口中。

        menubar = self.menuBar()  # 创建一个菜单栏对象，并将其添加到主窗口中。
        setMenu = menubar.addMenu('&设置')  # 在菜单栏中添加一个 "设置" 菜单，并设置快捷键为 "&设置"。
        setMenu.addAction(exitAct)  # 在 "设置" 菜单中添加一个 "Exit" 动作，即前面创建的 QAction 对象。
```

- 子菜单

```python
from PyQt6.QtWidgets import QMainWindow, QMenu, QApplication
from PyQt6.QtGui import QAction
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        setMenu = menubar.addMenu('设置')

        newAct = QAction('新建', self)

        impMenu = QMenu('导入', self)
        impCsv = QAction('导入CSV', self)
        impXlsx = QAction('导入xlsx', self)
        impMenu.addAction(impCsv)
        impMenu.addAction(impXlsx)
        
        setMenu.addAction(newAct)
        setMenu.addMenu(impMenu)  # 创建一个子菜单
```


- 勾选菜单

```python
        SMTAct = QAction('开启多线程', self, checkable=True)  # checkable=True 表示该动作是可勾选的。
        SMTAct.setStatusTip('多线程已开启')
        SMTAct.setChecked(True)  # 设置该动作的初始状态为选中状态
```

- 上下文菜单(鼠标右键弹出菜单)
```python
def contextMenuEvent(self, event):

        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        openAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec(self.mapToGlobal(event.pos()))  # 使用 exec 方法调出上下文菜单，通过鼠标事件对象获得鼠标坐标点event.pos()，再调用 mapToGlobal 方法把组件的坐标设置成全局的屏幕坐标。

        if action == quitAct:
            QApplication.instance().quit()
```

QFileDialog 选择文件对话窗口

#### QMessageBox 对话窗口

```python

from PyQt6.QtWidgets import QMainWindow, QMessageBox
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def closeEvent(self, event):  # 它将在窗口关闭时被调用，并传入一个名为 event 的参数，该参数包含关闭事件的详细信息。
        reply = QMessageBox.question(self, '提示',
                                     "你真的要退出吗", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:  # 该行根据用户单击的按钮来决定是否关闭应用程序。如果用户单击了 "是" 按钮，则事件被接受并关闭窗口，
            event.accept()
        else:
            event.ignore()   # 否则事件被忽略，窗口保持打开状态。
```
QInputDialog 输入窗口
QWebEngineView 显示网页组件


### 操作功能

下面这几篇文章，会介绍 PyQt6 里一些重要又好用的功能。

QTimer 定时器
QThread 多线程
QtCore.pyqtSignal 信号传递
QPainter 绘图
QPainter 绘图 （ QPen）
QPainter 绘图 （ 保存图片）
QtMultimedia 播放声音
QSS 样式设定
侦测鼠标事件
侦测键盘事件与快捷键组合
侦测与控制窗口
窗口中开启新窗口
显示图片的三种方法
显示 Matplotlib 图表（ 静态图表、图表动画）
显示 Pillow 图片
显示 OpenCV 图片和视频


### 接口布局方式

下面这几篇文章，会介绍 PyQt6 元件在接口的中三种布局方式。

#### Layout 布局（ 垂直和水平）

```python
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()  # 创建一个水平布局对象，并将其赋值给 hbox 变量。
        hbox.addStretch(1)  # 在水平布局中添加一个拉伸项，用于将按钮推到布局的最右边。
        hbox.addWidget(okButton)  # 将 okButton 按钮添加到水平布局中。
        hbox.addWidget(cancelButton)  # 将 cancelButton 按钮添加到水平布局中。

        vbox = QVBoxLayout()  # 创建一个垂直布局对象，并将其赋值给 vbox 变量。
        vbox.addStretch(1)  # 在垂直布局中添加一个拉伸项，用于将按钮推到布局的底部。
        vbox.addLayout(hbox)  # 将水平布局 hbox 添加到垂直布局 vbox 中。

        self.setLayout(vbox)  # 将窗口的布局设置为垂直布局 vbox，以便正确显示按钮。
```
注意：
addStretch(1) 是 QVBoxLayout 和 QHBoxLayout 类中的方法，用于向布局中添加一个拉伸项。该方法的参数是一个整数，用于指定拉伸项的弹簧因子。

弹簧因子决定了每个拉伸项在布局中所占的空间比例。

默认情况下，弹簧因子为0，表示不分配额外的空间给拉伸项。当设置为正整数时，所有拉伸项将按照弹簧因子进行分配，其中数值较大的拉伸项占用更多的空间。

在上述代码中，addStretch(1) 表示在布局中添加一个拉伸项，并将其弹簧因子设置为1。这意味着该拉伸项会占用相对较少的空间，而其他没有设置弹簧因子的部件将会以默认方式分配剩余的空间。

在实际应用中，可以根据需要使用不同的数字来调整拉伸项的弹簧因子，以实现期望的布局效果。例如，如果想要一个部件占用更多的空间，可以将其拉伸项的弹簧因子设置为较大的值。而如果希望某些部件固定大小，可以将其拉伸项的弹簧因子设置为0。

除了 0 和正整数外，还可以使用负数作为弹簧因子。负数的作用是将布局中的空间收缩到最小，以适应部件的最小尺寸。这在需要固定大小或者只允许部件占用一定空间的布局中非常有用。

总而言之，addStretch() 方法的作用是在布局中添加一个拉伸项，并根据设定的弹簧因子来分配和控制布局中的空间。


#### Layout 布局 （ Gird 网格）

QGridLayout 是最常用的布局类，它能把空间分为多行多列。

```python
import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        grid = QGridLayout()  # 创建一个网格布局对象 grid，用于将按钮放置在计算器界面上。
        self.setLayout(grid)  # 将计算器窗口的布局设置为 grid，即使用网格布局。

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']  # 定义了一个包含按钮名称的列表 names，其中包括计算器上的各个按钮的名称。

        positions = [(i, j) for i in range(5) for j in range(4)]  # 创建一个包含按钮位置的列表 positions，使用嵌套循环生成 5 行 4 列的网格位置

        for position, name in zip(positions, names):  # 使用 zip 函数同时迭代 positions 和 names 列表，将每个按钮的位置和名称进行配对。
 
            if name == '':  # 如果按钮的名称为空字符串，则跳过当前循环，不创建该按钮。
                continue

            button = QPushButton(name)  # 创建一个名为 name名称变量 的按钮对象。
            grid.addWidget(button, *position)  # 将按钮添加到网格布局中，并指定其位置为 position位置变量。


        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
```


```python
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)  # W4010E230779R000559728

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)  # 将reviewEdit控件添加到网格布局中，并指定它应该放在第3行、第1列，占据5行1列的位置（即跨越第3-7行、第1列）。

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
```


#### Layout 布局 （ Form 表单）



### 示例应用






下面这几篇文章，会通过 PyQt6 实际做出一些应用。

搭配 OpenCV 实作电脑摄影机
搭配 OpenCV 实作摄影机拍照和录像
搭配 pyaudio 实作简单录音机
小画家（ 可调整画笔颜色、粗细和存档）
打开图片转换（ 可调整质量和尺寸）
调整图片亮度对比、饱和度、锐利度
简单计算机
