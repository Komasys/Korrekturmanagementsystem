# Betriebshandbuch

## 3. Betrieb und Wartung

### 3.1 Updates und Backups

-   **Updates:**

    -   **Backend:**

        1. Ziehen Sie die neuesten Änderungen aus dem Git-Repository:
            ```sh
            git pull origin main
            ```
        2. Aktualisieren Sie die Python-Abhängigkeiten:
            ```sh
            source venv/bin/activate  # Windows: venv\Scripts\activate
            pip install --upgrade -r requirements.txt
            ```
        3. Führen Sie Datenbankmigrationen durch:
            ```sh
            flask db upgrade
            ```
        4. Starten Sie den Backend-Dienst neu:
            ```sh
            systemctl restart korrektur-backend
            ```

    -   **Frontend:**
        1. Ziehen Sie die neuesten Änderungen aus dem Git-Repository:
            ```sh
            git pull origin main
            ```
        2. Installieren Sie die Node.js-Abhängigkeiten:
            ```sh
            npm install
            ```
        3. Bauen Sie das Frontend neu:
            ```sh
            npm run build
            ```
        4. Kopieren Sie die Dateien in das Webserver-Verzeichnis und starten Sie den Webserver neu:
            ```sh
            cp -r dist /var/www/korrektur-frontend/
            systemctl restart nginx
            ```

-   **Backups:**
    -   **Datenbank:**
        Erstellen Sie regelmäßige Backups der PostgreSQL-Datenbank:
        ```sh
        pg_dump -U postgres -F c -b -v -f /path/to/backup.sqlc test_db
        ```
    -   **Dateien:**
        Sichern Sie den `uploads`-Ordner, der Anhänge enthält:
        ```sh
        tar -czvf uploads_backup.tar.gz uploads/
        ```

### 3.2 Benutzer- und Rechteverwaltung

-   **Benutzerverwaltung:**

    -   Benutzer können über die Datenbank direkt verwaltet werden. Beispiel:
        ```sql
        INSERT INTO benutzer (id, name, email, rolle, password_hash) VALUES (...);
        ```
    -   Alternativ können Sie ein Admin-Interface entwickeln, um Benutzerrollen zu ändern.

-   **Rechteverwaltung:**
    -   Rollen und Berechtigungen sind im System definiert (`backend/models/enums.py`).
        -   **Student:** Kann Tickets erstellen und eigene Tickets einsehen.
        -   **Tutor/Dozent:** Kann Tickets bearbeiten und kommentieren.
        -   **QM:** Kann Tickets prüfen und abschließen.
        -   **Admin:** Hat Vollzugriff.
    -   Änderungen an den Rollen können über die Datenbank vorgenommen werden:
        ```sql
        UPDATE benutzer SET rolle = 'ADMIN' WHERE email = 'example@example.com';
        ```

---

## 4. Fehlerbehebung

### 4.1 Analyse der Logs

-   **Backend-Logs:**

    -   Die Logs des Flask-Backends können über `journalctl` eingesehen werden:
        ```sh
        journalctl -u korrektur-backend
        ```
    -   Prüfen Sie Fehler wie fehlgeschlagene Datenbankverbindungen oder Syntaxfehler.

-   **Frontend-Logs:**

    -   Überprüfen Sie die Browser-Konsole (F12) auf JavaScript-Fehler.
    -   Logs des Webservers (z. B. Nginx):
        ```sh
        tail -f /var/log/nginx/error.log
        ```

-   **Datenbank-Logs:**
    -   PostgreSQL-Logs können unter `/var/log/postgresql/` eingesehen werden.

### 4.2 Häufige Probleme und Lösungen

-   **Problem:** Datenbankverbindung schlägt fehl.
    **Lösung:**

    -   Prüfen Sie die Umgebungsvariable `DATABASE_URL` in der `.env`-Datei.
    -   Stellen Sie sicher, dass der PostgreSQL-Dienst läuft:
        ```sh
        systemctl status postgresql
        ```

-   **Problem:** Frontend lädt nicht.
    **Lösung:**

    -   Prüfen Sie, ob das Frontend korrekt gebaut wurde (`npm run build`).
    -   Stellen Sie sicher, dass die Dateien im Webserver-Verzeichnis vorhanden sind.

-   **Problem:** Fehler bei Datenbankmigrationen.
    **Lösung:**

    -   Prüfen Sie den Alembic-Status:
        ```sh
        flask db current
        ```
    -   Reparieren Sie Migrationen:
        ```sh
        flask db stamp head
        flask db migrate
        flask db upgrade
        ```

-   **Problem:** Benutzer kann sich nicht anmelden.
    **Lösung:**
    -   Prüfen Sie, ob der Benutzer in der Datenbank existiert.
    -   Überprüfen Sie die Passwort-Hash-Funktion (`werkzeug.security`).
