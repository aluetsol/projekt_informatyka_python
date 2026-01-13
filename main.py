import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QSlider
    #, QFrame
)
from PyQt5.QtCore import Qt, QRectF, QPointF 
#QTimer, 

from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath


class Zbiornik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(350, 500)
        #self.setStyleSheet("background-color: #444;")
        self.top_h = 60
        self.mid_h = 200
        self.bot_h = 60

        self.w_top = 200
        self.w_mid = 140
        self.w_bot = 40

        self.total_h = self.top_h + self.mid_h + self.bot_h

        #self.level = 0.0
        self.level = 0.5
        #self.fill_open = False
        #self.drain_open = False
        #self.flow_rate = 0.004
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update_level)
        #self.timer.start(16)
        self.draw_x = 50
        self.deleteLaterraw_y = 50

    #def toggle_fill(self):
        #self.fill_open = not self.fill_open

    def setPolozenie(self, x, y):
        self.draw_x = x
        self.draw_y = y
        self.update()

    #def toggle_fill(self):
        #self.fill_open = not self.fill_open

    def toggle_drain(self):
        self.drain_open = not self.drain_open

    def reset(self):
        self.level = 0.0
        self.fill_open = False
        self.drain_open = False
        self.update()

    def setLevel(self, val):
        self.level = max(0.0, min(1.0, val))
        self.update()

   # def update_level(self):
        #if self.fill_open and self.level < 1.0:
            #self.level += self.flow_rate
       # if self.drain_open and self.level > 0.0:
            #self.level -= self.flow_rate

        #self.level = max(0.0, min(1.0, self.level))
        #self.update()
    def getPoziom(self):
        return self._poziom
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.draw_x + self.w_top / 2
        start_y = self.draw_y

        #path = QPainterPath()

        p1 = QPointF(cx - self.w_top/2, start_y)
        p2 = QPointF(cx + self.w_top/2, start_y)

        p3 = QPointF(cx + self.w_mid/2, start_y + self.top_h)
        p4 = QPointF(cx - self.w_mid/2, start_y + self.top_h)

        p5 = QPointF(cx + self.w_mid/2, start_y + self.top_h + self.mid_h)
        p6 = QPointF(cx - self.w_mid/2, start_y + self.top_h + self.mid_h)

        p7 = QPointF(cx + self.w_bot/2, start_y + self.total_h)
        p8 = QPointF(cx - self.w_bot/2, start_y + self.total_h)

        path = QPainterPath()
        for p in [p1, p2, p3, p5, p7, p8, p6, p4]:
            if path.isEmpty():
                path.moveTo(p)
            else:
                path.lineTo(p)
        path.closeSubpath()

        painter.save()
        painter.setClipPath(path)

        h = self.total_h * self.level
        rect_liquid = QRectF(
            cx - self.w_top/2,
            start_y + self.total_h - h,
            self.w_top,
            h
        )

        painter.fillRect(rect_liquid, QColor(0, 170, 255, 230))
        painter.restore()

        pen = QPen(Qt.white, 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)


class TankControlPanel(QWidget):
    def __init__(self, tank: Zbiornik):
        super().__init__()
        self.resize(800, 600)

        layout = QVBoxLayout()
        #layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)

        self.label = QLabel("Poziom: 0%")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        btns = QHBoxLayout()

        self.btn_fill = QPushButton("IN (zawór)")
        self.btn_fill.clicked.connect(self.tank.toggle_fill)
        btns.addWidget(self.btn_fill)

        self.btn_drain = QPushButton("OUT (zawór)")
        self.btn_drain.clicked.connect(self.tank.toggle_drain)
        btns.addWidget(self.btn_drain)

        self.btn_reset = QPushButton("RESET")
        self.btn_reset.clicked.connect(self.reset_all)
        btns.addWidget(self.btn_reset)

        layout.addLayout(btns)

        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update_label)
       # self.timer.start(100)

    def slider_changed(self, val):
        self.tank.setLevel(val / 100)

    def reset_all(self):
        self.tank.reset()
        self.slider.setValue(0)

    def update_label(self):
        percent = int(self.tank.level * 100)
        self.label.setText(f"Poziom: {percent}%")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zadanie 3 - Dwa Zbiorniki PyQt5")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #222; color: white;")

        layout = QHBoxLayout()
        self.setLayout(layout)
        
        layout.setSpacing(30)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        tank1_box = QVBoxLayout()
        self.tank1 = Zbiornik()
        tank1_box.addWidget(self.tank1)
        tank1_box.addWidget(TankControlPanel(self.tank1))
        layout.addLayout(tank1_box)

        tank2_box = QVBoxLayout()
        self.tank2 = Zbiornik()
        tank2_box.addWidget(self.tank2)
        tank2_box.addWidget(TankControlPanel(self.tank2))
        layout.addLayout(tank2_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
