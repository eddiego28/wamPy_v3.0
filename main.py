import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from publisher.pubGUI import PublisherTab
from subscriber.subGUI import SubscriberTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema WAMP: Publicador y Subscriptor")
        self.resize(900, 700)
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        self.publisherTab = PublisherTab(self)
        self.subscriberTab = SubscriberTab(self)
        tabs.addTab(self.publisherTab, "Publicador")
        tabs.addTab(self.subscriberTab, "Subscriptor")
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())