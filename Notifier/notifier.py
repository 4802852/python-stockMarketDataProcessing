import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import datetime
from os import path
from get_info import *

if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from slack.slack import *
else:
    from ..slack.slack import *
# from slack.slack import *


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.now = datetime.datetime.now()
        self.now_date = datetime.datetime.today().weekday()

        # timer
        self.t1 = self.now.replace(hour=20, minute=0, second=0, microsecond=0)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.setInterval(1 * 1000)
        self.timer.timeout.connect(self.timeout_run)

    def initUI(self):
        self.btn = QPushButton("Quit", self)
        self.btn.move(300, 60)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(QCoreApplication.instance().quit)

        # 시간을 표시할 라벨 생성
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 250, 20)
        self.label.move(40, 30)

        self.setWindowTitle("Notifier")
        self.move(300, 300)
        self.resize(400, 100)
        self.show()

    def timeout_run(self):
        self.now = datetime.datetime.now()
        self.now_date = datetime.datetime.today().weekday()
        self.t1 = self.now.replace(hour=20, minute=0, second=0, microsecond=0)
        text = self.now.strftime("%Y-%m-%d %H:%M:%S")
        self.label.setText(str(text))
        if self.now_date == 5 or self.now_date == 6:
            pass
        else:
            if self.t1 <= self.now < self.t1.replace(second=1):
                to_slack(self.get_inform(), "#exchange-rate")

    def get_inform(self):
        msg = get_message()
        return msg


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
