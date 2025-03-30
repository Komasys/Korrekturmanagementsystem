<template>
  <div class="container">
    <h1>Benutzerhandbuch für das Korrekturmanagementsystem</h1>

    <section>
      <h2>Einführung</h2>
      <p>
        Dieses Handbuch soll den Benutzern eine einfache und verständliche Anleitung zur Nutzung des
        Korrekturmanagementsystems bereitstellen. Es beschreibt alle notwendigen Schritte, um Fehler
        oder Verbesserungsvorschläge zu melden und den Bearbeitungsprozess zu verfolgen.
      </p>
      <p>
        <strong>Zielgruppe:</strong> Studierende der IU, die das System zur Meldung von Problemen in
        ihren Kursen verwenden.
      </p>
      <p><strong>Systemanforderungen:</strong></p>
      <ul>
        <li>Aktueller Webbrowser (z.B. Chrome, Firefox, Safari, Edge)</li>
        <li>Stabile Internetverbindung</li>
        <li>Gültiges IU-Benutzerkonto</li>
      </ul>
    </section>

    <section>
      <h2>Erste Schritte</h2>
      <h3>Anmeldung und Benutzerrollen</h3>
      <ul>
        <li><strong>Student:</strong> Eigene Tickets erstellen, einsehen, kommentieren</li>
        <li>
          <strong>Tutor & Dozent:</strong> Alle Tickets einsehen, kommentieren, Priorität/Status
          ändern, an QM weiterleiten
        </li>
        <li><strong>QM:</strong> Tickets einsehen/bearbeiten, Prioritäten setzen, kommentieren</li>
        <li><strong>Admin:</strong> Vollzugriff auf Systemfunktionen und Rollen</li>
      </ul>

      <h3>Überblick über die Benutzeroberfläche</h3>
      <ul>
        <li><strong>Ticket erstellen:</strong> Neues Ticket erfassen</li>
        <li><strong>Meine Tickets:</strong> Startseite nach Login, Übersicht & Bearbeitung</li>
        <li><strong>Logout:</strong> Abmeldung vom System</li>
        <li><strong>Hilfe:</strong> Unten links per <strong>?</strong>-Symbol erreichbar</li>
      </ul>

      <h3>Navigation im System</h3>
      <p>Die Navigation erfolgt über die Menüleiste am oberen Rand.</p>
    </section>

    <section>
      <h2>Meldungen erstellen und verwalten</h2>
      <h3>Fehler oder Verbesserungsvorschläge melden</h3>
      <ol>
        <li>In der Menüleiste auf <strong>Ticket erstellen</strong> klicken</li>
        <li>
          Formular ausfüllen:
          <ul>
            <li>Kategorie (z.B. Tippfehler, inhaltlicher Fehler)</li>
            <li>Kurs</li>
            <li>Lernmaterial</li>
            <li>Beschreibung</li>
            <li>Upload (z.B. Screenshots, max. 2 MB)</li>
          </ul>
        </li>
      </ol>

      <h3>Meldungen bearbeiten und ergänzen</h3>
      <ol>
        <li>In der Menüleiste auf <strong>Meine Tickets</strong> klicken</li>
        <li>Ticket auswählen und öffnen</li>
        <li>Kommentare hinzufügen</li>
      </ol>
    </section>

    <section>
      <h2>Bearbeitungsprozess und Statusverfolgung</h2>
      <ol>
        <li>Ticket öffnen</li>
        <li>Details wie Priorität und Status einsehen</li>
        <li>Historie und Kommentare im Ticketverlauf prüfen</li>
      </ol>
    </section>

    <section class="faq">
      <h2>Häufig gestellte Fragen (FAQ)</h2>
      <ul>
        <li>
          <strong>Fehlermeldung bei Anmeldung?</strong><br />Zugangsdaten und Internetverbindung
          prüfen.
        </li>
        <li><strong>Passwort vergessen?</strong><br />Wenden Sie sich an den Administrator.</li>
        <li><strong>Kein Ticket erstellen möglich?</strong><br />Pflichtfelder überprüfen.</li>
        <li>
          <strong>Wie kommentiere ich ein Ticket?</strong><br />Ticket öffnen, Kommentar unter
          „Rückfragen an Ticketersteller“ einfügen.
        </li>
        <li><strong>Rolle ändern?</strong><br />Nur Admins können Rollen ändern.</li>
      </ul>
    </section>

    <section>
      <h2>Support</h2>
      <p>Bei technischen Problemen wenden Sie sich bitte an das Projektteam.</p>
    </section>

    <div class="footer">
      <p><em>Dieses Handbuch soll Ihnen helfen, das System effektiv zu nutzen. Viel Erfolg!</em></p>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f9fafb;
  color: #111827;
}

h1,
h2,
h3 {
  color: #14dcc1;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

section {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
}

ul,
ol {
  padding-left: 1.5rem;
}

li + li {
  margin-top: 0.4rem;
}

p,
li {
  line-height: 1.6;
}

em {
  color: #6b7280;
}

code {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 90%;
}

.faq li {
  margin-bottom: 1rem;
}

.footer {
  text-align: center;
  font-size: 0.9rem;
  color: #6b7280;
}
</style>
