<template>
  <div class="container">
    <h1>Benutzerhandbuch für das Korrekturmanagementsystem</h1>

    <section>
      <h2>Einführung</h2>
      <p>
        Willkommen im Korrekturmanagementsystem! Dieses System unterstützt Sie bei der Verwaltung
        und Bearbeitung von Tickets zu Kursen und Lernmaterialien.
      </p>
    </section>

    <section>
      <h2>Rollen und Berechtigungen</h2>
      <ul>
        <li>
          <strong>Student:</strong>
          <ul>
            <li>Kann eigene Tickets erstellen und einsehen.</li>
            <li>Kann Kommentare zu eigenen Tickets hinzufügen.</li>
          </ul>
        </li>
        <li>
          <strong>Tutor & Dozent:</strong>
          <ul>
            <li>Können alle Tickets einsehen.</li>
            <li>Können Tickets kommentieren, Priorität/Status ändern und an QM weiterleiten.</li>
          </ul>
        </li>
        <li>
          <strong>QM (Prüfungsamt):</strong>
          <ul>
            <li>Kann alle Tickets einsehen und bearbeiten.</li>
            <li>Kann Prioritäten setzen, Status ändern und kommentieren.</li>
          </ul>
        </li>
        <li>
          <strong>Admin:</strong>
          <ul>
            <li>Vollzugriff auf Systemfunktionen und Benutzerrollen.</li>
          </ul>
        </li>
      </ul>
    </section>

    <section>
      <h2>Anmeldung</h2>
      <ol>
        <li>Öffnen Sie die Anmeldeseite.</li>
        <li>Geben Sie Ihre Zugangsdaten ein.</li>
        <li>Klicken Sie auf <strong>Login</strong>.</li>
        <li>Sie werden zum Dashboard weitergeleitet.</li>
      </ol>
    </section>

    <section>
      <h2>Dashboard</h2>
      <p>Ihre zentrale Übersicht. Funktionen variieren je nach Rolle:</p>
      <ul>
        <li><strong>Ticket erstellen</strong> (nur für Student, Dozent, Tutor, Admin)</li>
        <li><strong>Meine Tickets</strong> (nur für Student, Dozent, Tutor, Admin)</li>
        <li><strong>Bearbeitete Tickets</strong> (nur für Tutor, Dozent, QM, Admin)</li>
        <li><strong>Alle Tickets</strong> (nur für Tutor, Dozent, QM, Admin)</li>
      </ul>
    </section>

    <section>
      <h2>Ticket erstellen</h2>
      <ol>
        <li>Klicken Sie auf <strong>Ticket erstellen</strong>.</li>
        <li>
          Füllen Sie das Formular aus:
          <ul>
            <li>Kategorie (z.B. Tippfehler)</li>
            <li>Kurs</li>
            <li>Lernmaterial (optional)</li>
            <li>Beschreibung</li>
            <li>Datei-Upload (optional, max. 2 MB)</li>
          </ul>
        </li>
        <li>Absenden nicht vergessen!</li>
      </ol>
    </section>

    <section>
      <h2>Tickets verwalten</h2>
      <h3>Meine Tickets</h3>
      <ul>
        <li>Liste eigener Tickets mit Statusanzeige.</li>
      </ul>
      <h3>Bearbeitete Tickets</h3>
      <ul>
        <li>Nur für Bearbeiter sichtbar, inklusive Verlauf & Kommentare.</li>
      </ul>
      <h3>Alle Tickets</h3>
      <ul>
        <li>Nur für berechtigte Rollen.</li>
        <li>Filter- & Sortierfunktionen verfügbar.</li>
      </ul>
    </section>

    <section>
      <h2>Ticket bearbeiten</h2>
      <ol>
        <li>Ticket öffnen.</li>
        <li>
          Aktionen je nach Rolle:
          <ul>
            <li>Status ändern</li>
            <li>Priorität setzen</li>
            <li>Interne Beschreibung hinzufügen</li>
          </ul>
        </li>
        <li>Speichern nicht vergessen.</li>
      </ol>
    </section>

    <section>
      <h2>Kommentare hinzufügen</h2>
      <ol>
        <li>Ticket öffnen</li>
        <li>Zum Bereich <strong>Rückfragen an Ticketersteller</strong> scrollen</li>
        <li>Kommentar schreiben und hinzufügen</li>
      </ol>
    </section>

    <section>
      <h2>Benutzerhandbuch anzeigen</h2>
      <p>Jederzeit über das <strong>?</strong>-Symbol unten links erreichbar.</p>
    </section>

    <section>
      <h2>Abmeldung</h2>
      <ol>
        <li>Im Dashboard auf <strong>Logout</strong> klicken</li>
        <li>Sie werden abgemeldet</li>
      </ol>
    </section>

    <section class="faq">
      <h2>Häufig gestellte Fragen (FAQ)</h2>
      <ul>
        <li>
          <strong>Wie kann ich mein Passwort zurücksetzen?</strong><br />Wenden Sie sich an den
          Administrator.
        </li>
        <li>
          <strong>Wie kann ich meine Rolle ändern?</strong><br />Nur Administratoren können Rollen
          ändern.
        </li>
        <li>
          <strong>Wie kann ich ein Ticket kommentieren?</strong><br />Im Ticket unter
          <em>Rückfragen an Ticketersteller</em> kommentieren.
        </li>
      </ul>
    </section>

    <section>
      <h2>Support</h2>
      <p>Bei Fragen oder Problemen wenden Sie sich bitte an den Administrator.</p>
    </section>

    <div class="footer">
      <p>
        <em>Dieses Handbuch soll Ihnen helfen, das System effektiv zu nutzen. Viel Erfolg!</em>
      </p>
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
