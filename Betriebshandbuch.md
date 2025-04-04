# Betriebshandbuch

# 1. Einführung

## 1.1 Zweck und Zielgruppe

Dieses Betriebshandbuch beschreibt die Installation, Konfiguration, den Betrieb und die Wartung des Korrekturmanagementsystems, das im Rahmen der Qualitätssicherung für Lernmaterialien an der IU eingesetzt wird.
Ziel des Systems ist es, Studierenden die Möglichkeit zu geben, Fehler oder Unklarheiten in Lerninhalten strukturiert zu melden. Die Meldungen werden von Dozierenden oder Tutor:innen geprüft und – falls erforderlich – bearbeitet oder weitergeleitet.
Der gesamte Prozess wird über ein rollenbasiertes Ticketsystem verwaltet.

**Zielgruppe:**
Systemadministrator:innen, IT-Support-Mitarbeitende sowie ggf. technische Projektverantwortliche, die für den Betrieb und die Wartung des Systems zuständig sind.

## 1.2 Systemarchitektur

Das Korrekturmanagementsystem ist als webbasierte Client-Server-Architektur konzipiert.
Der Zugriff erfolgt über gängige Browser auf Desktop- und Mobilgeräten.
Die Systemarchitektur ist modular aufgebaut und trennt Frontend und Backend.

-   **Frontend**: Vue.js, kompiliert mit Vite
-   **Backend**: Flask, im Produktivbetrieb ergänzt durch Gunicorn
-   **Datenbank**: PostgreSQL (relationale SQL-Datenbank)
-   **Hosting**: Cloud-Server bei Hetzner
-   **Proxy**: Nginx als Reverse Proxy zur Weiterleitung externer Anfragen und Auslieferung statischer Inhalte

Eine Integration mit myCampus ist derzeit **nicht vorgesehen**, aber architektonisch möglich.
Die Architektur erfüllt Anforderungen an Benutzerfreundlichkeit, Skalierbarkeit und Zugänglichkeit.
Sicherheitsaspekte werden im Rahmen der prototypischen Umsetzung nur eingeschränkt berücksichtigt.

## 1.3 Technische Anforderungen

### Serverhardware (empfohlen)

-   **Prozessor**: 4 CPU-Kerne (z. B. Intel Xeon, AMD EPYC oder vergleichbar)
-   **Arbeitsspeicher (RAM)**: mindestens 8 GB
-   **Festplattenspeicher**: mindestens 50 GB verfügbarer Speicherplatz (SSD empfohlen)
-   **Netzwerkanbindung**: stabile Internetverbindung mit mindestens 10 Mbit/s im Up- und Download

### Infrastruktur

-   **Betriebssystem**: Linux (z. B. Ubuntu Server 20.04 LTS oder höher)
-   **Zugriff**: SSH-Zugang für Administratoren
-   **Erreichbarkeit**: Feste IP-Adresse oder dynamisches DNS, HTTPS-fähig
-   **Firewall**: Ports 80 (HTTP) und 443 (HTTPS) müssen offen sein
-   **Backup-Speicher**: externer Speicherort oder Netzlaufwerk für tägliche Sicherungen (optional)

### Virtualisierung (optional)

Das System kann auch in einer virtualisierten Umgebung (z. B. VMware, Proxmox, VirtualBox) oder containerisiert (z. B. Docker) betrieben werden.
In diesem Fall gelten die Ressourcenangaben für die virtuelle Instanz.

---

# 2. Installation und Einrichtung

## 2.1 Systemvoraussetzungen

Für die Entwicklung, Erweiterung und Wartung des Korrekturmanagementsystems müssen die folgenden Softwarekomponenten auf dem Entwicklungssystem installiert sein:

### Erforderliche Software

-   **Python** (Version 3.8 oder höher)
-   **Node.js** (Version 14 oder höher)
-   **npm** (Node Package Manager, wird mit Node.js installiert)
-   **PostgreSQL** (relationale Datenbank, Version 12 oder höher empfohlen)

### Empfohlene Entwicklungsumgebung

-   **Visual Studio Code (VS Code)**

### Empfohlene VS Code Erweiterungen

-   **Python** (offizielles Microsoft-Plugin)
-   **ESLint** (JavaScript-/TypeScript-Linter)
-   **Prettier – Code formatter** (zur einheitlichen Formatierung von Code)

Zusätzlich wird empfohlen, eine virtuelle Python-Umgebung (`venv` oder `poetry`) für die lokale Entwicklung zu verwenden, um Abhängigkeiten projektspezifisch zu verwalten.

## 2.2 Installationsanleitung

Die folgende Anleitung beschreibt die Schritte zur lokalen Installation und Ausführung des Korrekturmanagementsystems.
Die Anwendung besteht aus zwei Komponenten – **Backend** und **Frontend** – die separat eingerichtet werden.

### Installation des Backends

1. **Quellcode herunterladen**

    ```sh
    git clone https://github.com/Komasys/Korrekturmanagementsystem
    cd Korrekturmanagementsystem/backend
    ```

2. **Virtuelle Umgebung einrichten**

    ```sh
    python -m venv venv
    source venv/bin/activate  # Unter Windows: venv\Scripts\activate
    ```

3. **Abhängigkeiten installieren**

    ```sh
    pip install -r requirements.txt
    ```

4. **Datenbank vorbereiten**

    - Stellen Sie sicher, dass PostgreSQL installiert ist.
    - Legen Sie einen Datenbankbenutzer und eine Datenbank an.
    - Bearbeiten Sie die Datei `.env` im Backend-Verzeichnis und tragen Sie dort die Verbindungsdaten ein.

5. **Datenbankmigrationen ausführen**

    ```sh
    flask db upgrade
    ```

6. **Backend starten**
    ```sh
    flask run
    ```

### Installation des Frontends

1. **Zum Frontend-Verzeichnis wechseln**

    ```sh
    cd ../frontend
    ```

2. **Abhängigkeiten installieren**

    ```sh
    npm install
    ```

3. **Frontend starten**
    ```sh
    npm run dev
    ```

---

## 2.3 Grundkonfiguration

### Backend-Konfiguration

Die Backend-Konfiguration erfolgt über eine zentrale Python-Klasse (`Config`) sowie eine `.env`-Datei, in der Umgebungsvariablen gesetzt werden. Die wichtigsten Parameter in der `config.py` lauten:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB limit
```

#### Auszug aus `requirements.txt`:

```plaintext
Flask==3.1.0
Flask-JWT-Extended==4.7.1
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
gunicorn==23.0.0
psycopg2-binary==2.9.10
SQLAlchemy==2.0.38
python-dotenv==1.0.1
pytest==8.3.5
pylint==3.3.5
```

### Frontend-Konfiguration

Die Konfiguration erfolgt über `vite.config.js`:

```javascript
// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vueDevTools()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
});
```

#### `.editorconfig` zur Sicherstellung einheitlicher Formatierung:

```plaintext
[*.{js,jsx,mjs,cjs,ts,tsx,mts,cts,vue,css,scss,sass,less,styl}]
charset = utf-8
indent_size = 2
indent_style = space
insert_final_newline = true
trim_trailing_whitespace = true
end_of_line = lf
max_line_length = 100
```

---

## Nützliche Befehle für Entwicklung und Qualitätssicherung

-   **Backend-Tests ausführen (Work in Progress):**

    ```sh
    pytest
    ```

-   **Backend-Codeanalyse (Linting):**

    ```sh
    pylint backend
    ```

-   **Frontend-Codeanalyse (Linting):**

    ```sh
    npm run lint
    ```

-   **Frontend-Codeformatierung:**
    ```sh
    npm run format
    ```

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
