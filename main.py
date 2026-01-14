import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Rura:
    def __init__(self, punkty, grubosc=12):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = QColor(160, 160, 160)
        self.kolor_cieczy = QColor(0, 180, 255)
        self.czy_plynie = False

    def ustaw_przeplyw(self, plynie):
        self.czy_plynie = plynie

    def draw(self, painter):
        if len(self.punkty) < 2:
            return

        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)

        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen_rura)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)
            painter.drawPath(path)

class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0

    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def czy_pusty(self): return self.aktualna_ilosc <= 0.1

    def czy_pelny(self): return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def punkt_gora_srodek(self): return (self.x + self.width / 2, self.y)

    def punkt_dol_srodek(self): return (self.x + self.width / 2, self.y + self.height)

    def draw(self, painter):
        if self.poziom > 0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 120, 255, 200))
            painter.drawRect(int(self.x + 3), int(y_start), int(self.width - 6), int(h_cieczy-2))

        pen = QPen(Qt.white, 4)
        pen.setJoinStyle(Qt.MiterJoin )
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.x, self.y, self.width, self.height)
        painter.setPen(Qt.white)
        painter.drawText(self.x, self.y - 10, self.nazwa)

class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaskada : Dol -> Gora")
        self.setFixedSize(900, 680)
        self.setStyleSheet("background-color: #e5e5e5;")

        self.z1 = Zbiornik(50, 50, nazwa="Zbiornik 1")
        self.z1.aktualna_ilosc = 100
        self.z1.aktualizuj_poziom()

        self.z2 = Zbiornik(350, 200, nazwa="Zbiornik 2")
        self.z3 = Zbiornik(650, 350, nazwa="Zbiornik 3")
        self.zbiorniki = [self.z1, self.z2, self.z3]

        self.rura1 = self.stworz_rure(self.z1, self.z2)
        self.rura2 = self.stworz_rure(self.z2, self.z3)
        self.rury = [self.rura1, self.rura2]
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)
        self.running = False
        self.flow_speed = 1.0
        self.btn_start = QPushButton("Start / Stop", self)
        self.btn_start.setGeometry(50, 540, 120, 30)
        self.btn_start.clicked.connect(self.toggle)
        self.stworz_przyciski_reczne()

    def stworz_rure(self, z_gora, z_dol):
        p1 = z_gora.punkt_dol_srodek()
        p2 = z_dol.punkt_gora_srodek()
        mid_y = (p1[1] + p2[1]) / 2

        return Rura([
            p1,
            (p1[0], mid_y),
            (p2[0], mid_y),
            p2
        ])

    def stworz_przyciski_reczne(self):
        x = 220
        for z in self.zbiorniki:
            btn_fill = QPushButton(f"+ {z.nazwa}", self)
            btn_empty = QPushButton(f"- {z.nazwa}", self)

            btn_fill.setGeometry(x, 520, 130, 30) 
            btn_empty.setGeometry(x , 570, 130, 30)
            btn_fill.clicked.connect(lambda _, zb=z: self.napelnij(zb))
            btn_empty.clicked.connect(lambda _, zb=z: self.oproznij(zb))

            x += 200
    
    def napelnij(self, zb):
        zb.aktualna_ilosc = zb.pojemnosc
        zb.aktualizuj_poziom()
        self.update()

    def oproznij(self, zb):
        zb.aktualna_ilosc = 0
        zb.aktualizuj_poziom()
        self.update()

    def toggle(self):
        if self.running:
            self.timer.stop()
        else:
            self.timer.start(30)
        self.running = not self.running

    def logika_przeplywu(self):
        plynie1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            il = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(il)
            plynie1 = True
        self.rura1.ustaw_przeplyw(plynie1)

        plynie2 = False
        if self.z2.aktualna_ilosc > 5 and not self.z3.czy_pelny():
            il = self.z2.usun_ciecz(self.flow_speed)
            self.z3.dodaj_ciecz(il)
            plynie2 = True
        self.rura2.ustaw_przeplyw(plynie2)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for r in self.rury:
            r.draw(painter)
        for z in self.zbiorniki:
            z.draw(painter)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SymulacjaKaskady()
    window.show()
    sys.exit(app.exec_())
