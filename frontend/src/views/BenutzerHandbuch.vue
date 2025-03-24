<template>
  <div class="handbuch">
    <h1>Benutzerhandbuch</h1>
    <section>
      <h2>Einführung</h2>
      <p>
        Willkommen im Korrekturmanagementsystem. Dieses Handbuch soll Ihnen helfen, sich mit den
        grundlegenden Funktionen des Systems vertraut zu machen.
      </p>
    </section>
    <section>
      <h2>Anmeldung</h2>
      <p>
        Um sich anzumelden, geben Sie Ihre E-Mail-Adresse und Ihr Passwort auf der Anmeldeseite ein.
      </p>
    </section>
    <section>
      <h2>Dashboard</h2>
      <p>
        Nach der Anmeldung gelangen Sie zum Dashboard. Hier können Sie Tickets erstellen, Ihre
        eigenen Tickets einsehen und alle Tickets verwalten (abhängig von Ihrer Rolle).
      </p>
    </section>
    <section>
      <h2>Ticket erstellen</h2>
      <p>
        Um ein neues Ticket zu erstellen, klicken Sie auf "Ticket erstellen" im Dashboard. Füllen
        Sie das Formular aus und klicken Sie auf "Absenden".
      </p>
    </section>
    <section>
      <h2>Tickets verwalten</h2>
      <p>
        Sie können Ihre eigenen Tickets unter "Meine Tickets" einsehen. Abhängig von Ihrer Rolle
        können Sie auch alle Tickets unter "Alle Tickets" einsehen und bearbeiten.
      </p>
    </section>
    <section>
      <h2>Abmelden</h2>
      <p>
        Um sich abzumelden, klicken Sie auf "Logout" im Dashboard. Dadurch werden Sie vom System
        abgemeldet und zur Anmeldeseite zurückgeleitet.
      </p>
    </section>
    <section>
      <h2>Rollen und Berechtigungen</h2>
      <p>
        Das System unterscheidet zwischen verschiedenen Rollen, die unterschiedliche Berechtigungen
        haben:
      </p>
      <ul>
        <li><strong>Student:</strong> Kann eigene Tickets erstellen und einsehen.</li>
        <li>
          <strong>Tutor:</strong> Kann alle Tickets einsehen, aber nur beschränkt bearbeiten bzw. an
          QM weiterleiten. Kann zudem Tickets erstellen.
        </li>
        <li>
          <strong>Dozent:</strong> Kann alle Tickets einsehen, aber nur beschränkt bearbeiten bzw.
          an QM weiterleiten. Kann zudem Tickets erstellen.
        </li>
        <li><strong>QM:</strong> Kann alle Tickets einsehen und bearbeiten.</li>
        <li>
          <strong>Admin:</strong> Hat volle Kontrolle über das System und kann alle Einstellungen
          vornehmen.
        </li>
      </ul>
    </section>
    <section>
      <h2>Häufig gestellte Fragen (FAQ)</h2>
      <h3>Wie kann ich mein Passwort zurücksetzen?</h3>
      <p>
        Wenn Sie Ihr Passwort vergessen haben, wenden Sie sich bitte an den Administrator Ihres
        Systems, um es zurückzusetzen.
      </p>
      <h3>Wie kann ich meine Rolle ändern?</h3>
      <p>
        Rollenänderungen können nur von einem Administrator vorgenommen werden. Bitte wenden Sie
        sich an den Administrator Ihres Systems.
      </p>
      <h3>Wie kann ich ein Ticket kommentieren?</h3>
      <p>
        Um ein Ticket zu kommentieren, öffnen Sie das Ticket und fügen Sie Ihren Kommentar im
        entsprechenden Abschnitt hinzu.
      </p>
    </section>
  </div>
</template>

<script setup></script>

<style scoped>
.handbuch {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1,
h2 {
  color: #333;
}

p {
  line-height: 1.6;
  color: #555;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
}

h3 {
  color: #444;
  margin-top: 20px;
}
</style>
