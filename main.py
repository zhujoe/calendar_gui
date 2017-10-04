# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime


class windowUI(QWidget):

    def __init__(self):
        super(windowUI, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口样式
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置窗口为透明（配合窗口阴影，在这里窗口并没有透明化）
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置托盘选项
        self.build_tray()
        # 初始化大小
        self.resize(345, 275+75+75)
        # 初始化位置
        self.central()

        # 添加窗口控件
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)

        self.timer = QTimer()

        self.days = QLCDNumber(3, self)
        self.days.setGeometry(60, 345, 70, 50)
        self.days.setSegmentStyle(QLCDNumber.Filled)
        self.displaydays()
        self.timer.timeout.connect(self.displaydays)

        self.days2 = QLCDNumber(7, self)
        self.days2.setGeometry(130, 345, 175, 50)
        self.days2.setSegmentStyle(QLCDNumber.Flat)
        self.displaydays2()
        self.timer.timeout.connect(self.displaydays2)

        self.times = QLCDNumber(8, self)
        self.times.setGeometry(80, 270, 200, 50)
        self.times.setSegmentStyle(QLCDNumber.Flat)
        self.display()

        self.timer.timeout.connect(self.display)
        # self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.display)
        self.timer.start(1000)


        # splitter1 = QSplitter(Qt.Horizontal)
        # splitter1.addWidget(self.days)
        # splitter1.addWidget(self.days2)

    def displaydays(self):
        d1 = datetime.now()
        d2 = datetime(2017, 8, 18)
        self.days.display((d2-d1).days+1)

    def displaydays2(self):
        d1 = datetime.now()
        d2 = datetime(2017, 8, 18)
        self.days2.display((d2-d1).total_seconds())

    def display(self):
        current = QTime.currentTime()
        self.times.display(current.toString('HH:mm:ss'))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = QMouseEvent.globalPos()-self.pos()
            QMouseEvent.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False

    def build_tray(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('logo.png'))
        self.trayIcon.show()
        self.trayIcon.setToolTip('日历')
        self.trayIcon.activated.connect(self.trayClick)

        menu = QMenu()

        # 菜单选项
        normal = menu.addAction('显示到桌面')
        mini = menu.addAction('最小化到托盘')
        initxy = menu.addAction('回到右上角')
        offtop = menu.addAction('取消置顶')
        ontop = menu.addAction('置顶')
        exitA = menu.addAction('退出')

        # 事件
        normal.triggered.connect(self.showNormal)
        mini.triggered.connect(self.showMinimized)
        initxy.triggered.connect(self.showinitxy)
        offtop.triggered.connect(self.ushowtop)
        ontop.triggered.connect(self.showtop)
        exitA.triggered.connect(self.exit)

        self.trayIcon.setContextMenu(menu)

    def showtop(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        super(windowUI, self).showNormal()

    def ushowtop(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        super(windowUI, self).showNormal()

    def exit(self):
        self.trayIcon.setVisible(False)
        sys.exit(0)

    def showNormal(self):
        super(windowUI, self).showNormal()
        self.repaint()

    def central(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(screen.width() - size.width(), 0)
        # self.move(0, 0)

    def showinitxy(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = screen.width() - size.width()
        x1 = self.pos().x()
        y1 = self.pos().y()
        if x1 < x+1:
            for xy_x in range(x1, x+1, 2):
                self.move(xy_x, y1)
        else:
            for xy_x in range(x1, x+1, -2):
                self.move(xy_x, y1)
        if y1 > 1:
            for xy_y in range(y1, 1, -2):
                self.move(xy_x, xy_y)
        else:
            for xy_y in range(y1, 1, 2):
                self.move(xy_x, xy_y)

    def trayClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.repaint()

    def drawShadow(self, painter):
        # 阴影宽度
        self.SHADOW_WIDTH = 15
        # 绘制左上角、左下角、右上角、右下角、上、下、左、右边框
        self.pixmaps = list()
        self.pixmaps.append(str("./img/shadow/left_top.png"))
        self.pixmaps.append(str("./img/shadow/left_bottom.png"))
        self.pixmaps.append(str("./img/shadow/right_top.png"))
        self.pixmaps.append(str("./img/shadow/right_bottom.png"))
        self.pixmaps.append(str("./img/shadow/top_mid.png"))
        self.pixmaps.append(str("./img/shadow/bottom_mid.png"))
        self.pixmaps.append(str("./img/shadow/left_mid.png"))
        self.pixmaps.append(str("./img/shadow/right_mid.png"))

        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))   #左上角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[2]))   #右上角
        painter.drawPixmap(0,self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[1]))   #左下角
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  #右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH)) #左
        painter.drawPixmap(self.width()-self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH, self.height()- 2*self.SHADOW_WIDTH)) #右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[4]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH)) #上
        painter.drawPixmap(self.SHADOW_WIDTH, self.height()-self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width()-2*self.SHADOW_WIDTH, self.SHADOW_WIDTH))   #下

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawShadow(painter)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(QRect(self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.width()-2*self.SHADOW_WIDTH, self.height()-2*self.SHADOW_WIDTH))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = windowUI()
    window.show()
    sys.exit(app.exec_())
