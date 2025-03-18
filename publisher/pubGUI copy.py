def sendMessage(self):
    # Obtener el realm seleccionado
    selected_realms = []
    for r in range(self.realmTable.rowCount()):
        r_item = self.realmTable.item(r, 0)
        if r_item and r_item.checkState() == Qt.Checked:
            selected_realms.append(r_item.text().strip())

    # Si no hay ningún realm seleccionado, mostrar error
    if not selected_realms:
        QMessageBox.warning(self, "Advertencia", "Debes seleccionar al menos un Realm.")
        return

    # Obtener los topics seleccionados de cada realm
    selected_topics_by_realm = {}
    for realm in selected_realms:
        selected_topics_by_realm[realm] = []
        for t in range(self.topicTable.rowCount()):
            t_item = self.topicTable.item(t, 0)
            if t_item and t_item.checkState() == Qt.Checked:
                selected_topics_by_realm[realm].append(t_item.text().strip())

    # Si no hay topics seleccionados, mostrar error
    if all(len(topics) == 0 for topics in selected_topics_by_realm.values()):
        QMessageBox.warning(self, "Advertencia", "Debes seleccionar al menos un Topic en cada Realm marcado.")
        return

    # Obtener el contenido del mensaje
    content_text = self.editorWidget.jsonPreview.toPlainText()
    try:
        content = json.loads(content_text)
    except Exception as e:
        QMessageBox.critical(self, "Error", f"El JSON no es válido:\n{e}")
        return

    # Obtener modo de publicación y retraso
    mode = self.modeCombo.currentText()
    time_str = self.timeEdit.text().strip()
    delay = 0
    if mode == "Programado":
        try:
            h, m, s = map(int, time_str.split(":"))
            delay = h * 3600 + m * 60 + s
        except:
            delay = 0

    # Publicar en cada Realm y Topic marcado
    for realm in selected_realms:
        router_url = self.publisherTab.realms_topics.get(realm, {}).get("router_url", "ws://127.0.0.1:60001/ws")
        for topic in selected_topics_by_realm[realm]:
            start_publisher(router_url, realm, topic)
            send_message_now(topic, content, delay)

    # Registrar en la tabla de mensajes enviados
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details = json.dumps({
        "realms": selected_realms,
        "topics": selected_topics_by_realm,
        "content": content,
        "mode": mode,
        "time": time_str
    }, indent=2, ensure_ascii=False)

    self.publisherTab.viewer.add_message(", ".join(selected_realms), ", ".join(
        [", ".join(selected_topics_by_realm[r]) for r in selected_realms]), timestamp, details)

    print(f"✅ Mensaje publicado en realms {selected_realms} con topics {selected_topics_by_realm} a las {timestamp}")
