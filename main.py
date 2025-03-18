# interface/mainGUI.py
import sys, os, json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from publisher.pubGUI import PublisherTab
from subscriber.subGUI import SubscriberTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema WAMP: Publicador y Suscriptor")
        self.resize(900, 700)
        self.initUI()
        self.loadRealmTopicConfig()  # Carga el archivo de configuración al iniciar

    def initUI(self):
        centralWidget = QWidget()
        mainLayout = QVBoxLayout(centralWidget)
        self.tabs = QTabWidget()
        self.publisherTab = PublisherTab(self)
        self.subscriberTab = SubscriberTab(self)
        self.tabs.addTab(self.publisherTab, "Publicador")
        self.tabs.addTab(self.subscriberTab, "Suscriptor")
        mainLayout.addWidget(self.tabs)

        # Botones para cargar y guardar el proyecto
        projLayout = QHBoxLayout()
        self.loadProjButton = QPushButton("Cargar Proyecto")
        self.loadProjButton.clicked.connect(self.loadProject)
        projLayout.addWidget(self.loadProjButton)
        self.saveProjButton = QPushButton("Guardar Proyecto")
        self.saveProjButton.clicked.connect(self.saveProject)
        projLayout.addWidget(self.saveProjButton)
        mainLayout.addLayout(projLayout)

        self.setCentralWidget(centralWidget)

    def loadRealmTopicConfig(self):
        # Se carga el archivo de configuración ubicado en config\realms_topic_config.json
        config_path = os.path.join("config", "realm_topic_config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            realms_data = data.get("realms", {})
            if realms_data:
                # Se almacena la configuración en el SubscriberTab
                self.subscriberTab.realms_data = realms_data
                self.subscriberTab.realmCombo.clear()
                for realm_name in realms_data.keys():
                    self.subscriberTab.realmCombo.addItem(realm_name)
                # Se actualizan router URL y topics para el primer realm
                first_realm = list(realms_data.keys())[0]
                self.subscriberTab.urlEdit.setText(realms_data[first_realm].get("router_url", ""))
                self.subscriberTab.topicsList.clear()
                for topic in realms_data[first_realm].get("topics", []):
                    self.subscriberTab.topicsList.addItem(topic)
        except Exception as e:
            print(f"Error al cargar realm_topic_config: {e}")

    def loadProject(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Cargar Proyecto", "", "JSON Files (*.json);;All Files (*)")
        if not filepath:
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                proj = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el proyecto:\n{e}")
            return
        pub_config = proj.get("publisher", {})
        self.publisherTab.loadProjectFromConfig(pub_config)
        sub_config = proj.get("subscriber", {})
        self.subscriberTab.loadProjectFromConfig(sub_config)
        QMessageBox.information(self, "Proyecto", "Proyecto cargado correctamente.")

    def saveProject(self):
        proj_config = self.getProjectConfig()
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Proyecto", "", "JSON Files (*.json);;All Files (*)")
        if not filepath:
            return
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(proj_config, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Proyecto", "Proyecto guardado correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el proyecto:\n{e}")

    def getProjectConfig(self):
        pub_config = self.publisherTab.getProjectConfig()
        sub_config = self.subscriberTab.getProjectConfigLocal()
        return {"publisher": pub_config, "subscriber": sub_config}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
