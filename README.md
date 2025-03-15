# Korrekturmanagementsystem

## Projektübersicht

Dieses Projekt ist ein Korrekturmanagementsystem, das aus einem Backend (Flask) und einem Frontend (Vue.js) besteht.

## Voraussetzungen

Stellen Sie sicher, dass die folgenden Softwarekomponenten auf Ihrem System installiert sind:

-   Python 3.8 oder höher
-   Node.js 14 oder höher
-   npm (Node Package Manager)
-   PostgreSQL

### Benötigte VSCode Plugins

-   Python
-   ESLint
-   Prettier - Code formatter

## Backend Initialisierung

1. **Repository klonen:**

    ```sh
    git clone https://github.com/Komasys/Korrekturmanagementsystem
    cd Korrekturmanagementsystem/backend
    ```

2. **Virtuelle Umgebung erstellen und aktivieren:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Abhängigkeiten installieren:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Datenbank konfigurieren:**

    Stellen Sie sicher, dass PostgreSQL läuft und erstellen Sie eine Datenbank. Aktualisieren Sie die `.env` Datei mit Ihren Datenbankinformationen.

5. **Datenbankmigrationen durchführen:**

    ```sh
    flask db upgrade
    ```

6. **Backend starten:**

    ```sh
    flask run
    ```

## Frontend Initialisierung

1. **Zum Frontend-Verzeichnis wechseln:**

    ```sh
    cd ../frontend
    ```

2. **Abhängigkeiten installieren:**

    ```sh
    npm install
    ```

3. **Frontend starten:**

    ```sh
    npm run dev
    ```

## Nützliche Befehle

-   **Backend Tests ausführen (Work in Progress):**

    ```sh
    pytest
    ```

-   **Backend Linting:**

    ```sh
    pylint backend
    ```

-   **Frontend Linting:**

    ```sh
    npm run lint
    ```

-   **Frontend Formatierung:**

    ```sh
    npm run format
    ```

## Weitere Informationen

Weitere Informationen zur Projektstruktur und zu den einzelnen Komponenten finden Sie in den jeweiligen README-Dateien im `backend` und `frontend` Verzeichnis.
