# common/utils.py
import os, json
from PyQt5.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem, QVBoxLayout

def log_to_file(timestamp, topic, realm, message_json):
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    file_path = os.path.join(log_folder, "log.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {realm} | {topic} | {message_json}\n")

class JsonDetailDialog(QDialog):
    def __init__(self, json_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalle JSON")
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Clave", "Valor"])
        layout.addWidget(self.tree)
        self.setLayout(layout)
        try:
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data
        except Exception as e:
            data = {"error": str(e)}
        self.populateTree(data, self.tree.invisibleRootItem())
        self.tree.expandAll()  # Expande todo el árbol

    def populateTree(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent, [str(key), ""])
                self.populateTree(value, item)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                item = QTreeWidgetItem(parent, [f"[{index}]", ""])
                self.populateTree(value, item)
        else:
            QTreeWidgetItem(parent, ["", str(data)])
