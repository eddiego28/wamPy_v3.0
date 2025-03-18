import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from publisher.pubGUI import PublisherTab
from subscriber.subGUI import SubscriberTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema WAMP: Publicador y Suscriptor")
        self.setGeometry(100, 100, 1200, 800)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.publisherTab = PublisherTab()
        self.subscriberTab = SubscriberTab()
        
        self.tabs.addTab(self.publisherTab, "Publicador")
        self.tabs.addTab(self.subscriberTab, "Suscriptor")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
