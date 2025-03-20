<template>
  <div class="card">
    <h2>Ticket Details</h2>
    <p style="color: darkred; font-weight: 600">
      Hier folgen noch Historie, Kommentare, Bearbeitungsfunktion, Statusändernungen, Kurs-ID zeigt
      dann nicht die Nummer sondern den Namen etc. pp
    </p>
    <p><strong>ID:</strong> {{ ticket.id }}</p>
    <p><strong>Erstellt von:</strong> {{ ticket.ersteller_name }}</p>
    <p><strong>Erstellt am:</strong> {{ new Date(ticket.erstelldatum).toLocaleString() }}</p>
    <p><strong>Kurs:</strong> {{ ticket.kurs_name }}</p>
    <p><strong>Kategorie:</strong> {{ ticket.kategorie }}</p>
    <p><strong>Beschreibung:</strong> {{ ticket.beschreibung }}</p>
    <button>{{ ticket.status }}</button>
    <button>{{ ticket.prioritaet }}</button>
    <p>---Anhang coming soon---</p>
  </div>

  <div class="card">
    <h2>Interne Kommunikation</h2>
    <div v-for="eintrag in ticket.historie" :key="eintrag.id" class="comment">
      <p>
        <strong>{{ eintrag.bearbeiter_name }}</strong> am
        {{ new Date(eintrag.geaendert_am).toLocaleString() }}
      </p>
      <p>{{ eintrag.beschreibung }}</p>
      <p>{{ eintrag.status }}</p>
    </div>
    <form @submit.prevent="submitEdit">
      <div>
        <p style="color: darkred">Status- und Prioänderungen müssen noch implementiert werden</p>
        <label for="status">Status:</label>
        <select v-model="ticket.new_status" id="status">
          <option value="ABGELEHNT">Abgelehnt</option>
          <option value="PRUEFUNG">Prüfung</option>
          <option value="ANPASSUNG">Anpassung</option>
          <option value="GESCHLOSSEN">Geschlossen</option>
        </select>
      </div>
      <div>
        <label for="prioritaet">Priorität:</label>
        <select v-model="ticket.new_prioritaet" id="prioritaet">
          <option value="NIEDRIG">Niedrig</option>
          <option value="MITTEL">Mittel</option>
          <option value="HOCH">Hoch</option>
        </select>
      </div>
      <div>
        <label for="beschreibung">Beschreibung:</label>
        <textarea
          v-model="historieBeschreibung"
          id="beschreibung"
          placeholder="Beschreibung hinzufügen"
        ></textarea>
      </div>
      <button type="submit">Änderungen speichern</button>
    </form>
  </div>

  <div class="card">
    <h2>Rückfragen an Ticketersteller</h2>
    <div v-for="kommentar in ticket.kommentare" :key="kommentar.id" class="comment">
      <p>
        <strong>{{ kommentar.benutzer_name }}</strong> am
        {{ new Date(kommentar.erstelldatum).toLocaleString() }}
      </p>
      <p>{{ kommentar.nachricht }}</p>
    </div>
    <form @submit.prevent="submitComment">
      <textarea v-model="newComment" placeholder="Kommentar hinzufügen"></textarea>
      <button type="submit">Kommentar hinzufügen</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  ticketId: String,
})

const ticket = ref({})
const newComment = ref('')
const historieBeschreibung = ref('')
const userStore = useUserStore()

const loadTicketDetails = async () => {
  if (!props.ticketId) return
  const response = await fetch(`${API_URL}/ticket/getTicket/${props.ticketId}`)
  if (response.ok) {
    const data = await response.json()
    ticket.value = data
  } else {
    console.error('Failed to load ticket details')
  }
}

const submitComment = async () => {
  const response = await fetch(`${API_URL}/ticket/addComment`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      benutzer_id: userStore.benutzer_id,
      ticket_id: props.ticketId,
      nachricht: newComment.value,
    }),
  })

  if (response.ok) {
    newComment.value = ''
    loadTicketDetails()
  } else {
    console.error('Failed to add comment')
  }
}

const submitEdit = async () => {
  const response = await fetch(`${API_URL}/ticket/updateTicket`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ticket_id: props.ticketId,
      status: ticket.value.new_status,
      prioritaet: ticket.value.new_prioritaet,
      beschreibung: historieBeschreibung.value,
      bearbeiter_id: userStore.benutzer_id,
    }),
  })

  if (response.ok) {
    historieBeschreibung.value = ''
    loadTicketDetails()
  } else {
    console.error('Failed to update ticket')
  }
}

watch(() => props.ticketId, loadTicketDetails, { immediate: true })
</script>

<style scoped>
.card {
  width: 100%;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

h2 {
  color: #333;
  font-size: 1.5em;
  margin-bottom: 8px;
}

p {
  color: #555;
  line-height: 1.6;
}

p strong {
  color: #333;
}

p:last-child {
  color: #999;
  font-style: italic;
}

.comment {
  margin-bottom: 16px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

form {
  margin-top: 16px;
}

textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  resize: vertical;
  min-height: 100px;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

select {
  width: 100%;
  padding: 8px;
  margin-bottom: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

label {
  display: block;
  margin-bottom: 4px;
  color: #333;
  font-weight: bold;
}
</style>
