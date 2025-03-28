<template>
  <div class="card">
    <h2>Ticket Details</h2>
    <p><strong>ID:</strong> {{ ticket.id }}</p>
    <p><strong>Erstellt von:</strong> {{ capitalize(ticket.ersteller_name) }}</p>
    <p><strong>Erstellt am:</strong> {{ new Date(ticket.erstelldatum).toLocaleString() }}</p>
    <p><strong>Kurs:</strong> {{ ticket.kurs_name }}</p>
    <p><strong>Kategorie:</strong> {{ capitalize(ticket.kategorie) }}</p>
    <p><strong>Beschreibung:</strong> {{ ticket.beschreibung }}</p>
    <div v-if="ticket.anhaenge && ticket.anhaenge.length > 0">
      <h2>Anhänge</h2>
      <ul>
        <li v-for="anhang in ticket.anhaenge" :key="anhang.id">
          <a :href="`${API_URL}/uploads/${anhang.dateiname}`" target="_blank">{{
            anhang.dateiname
          }}</a>
        </li>
      </ul>
    </div>
    <div v-else>
      <p style="color: #999; font-style: italic">Keine Anhänge vorhanden</p>
    </div>
    <button class="btn1" :class="getPriorityClass(ticket.prioritaet)">
      {{ ticket.prioritaet }}
    </button>
    <button class="btn1" :class="getStatusClass(ticket.status)">{{ ticket.status }}</button>
  </div>

  <div class="card">
    <h2>Historie</h2>
    <div v-for="eintrag in ticket.historie" :key="eintrag.id" class="comment">
      <p>
        <strong>{{ capitalize(eintrag.bearbeiter_name) }}</strong> am
        {{ new Date(eintrag.geaendert_am).toLocaleString() }} | Status:
        {{ capitalize(eintrag.status) }}
      </p>
      <p>{{ eintrag.beschreibung }}</p>
    </div>
    <form @submit.prevent="submitEdit" v-if="canEditTicket">
      <div>
        <h2>Interne Kommunikation</h2>

        <p style="color: darkred"></p>
        <label for="status">Status:</label>
        <select v-model="new_status" id="status" required>
          <option value="PRÜFUNG">Prüfung (Tutor/Dozent)</option>
          <option value="ANPASSUNG">Anpassung (QM/Prüfungsamt)</option>
          <option value="ABGELEHNT">Abgelehnt</option>
          <option value="GESCHLOSSEN">Geschlossen</option>
        </select>
      </div>
      <div>
        <label for="prioritaet">Priorität:</label>
        <select v-model="new_prioritaet" id="prioritaet">
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
    <div v-if="ticket.kommentare && ticket.kommentare.length > 0">
      <div v-for="kommentar in ticket.kommentare" :key="kommentar.id" class="comment">
        <p>
          <strong>{{ kommentar.benutzer_name }}</strong> am
          {{ new Date(kommentar.erstelldatum).toLocaleString() }}
        </p>
        <p>{{ kommentar.nachricht }}</p>
      </div>
    </div>
    <div v-else>
      <p style="color: #999; font-style: italic">Keine Kommentare vorhanden</p>
    </div>
    <form @submit.prevent="submitComment" v-if="canSubmitComment">
      <textarea v-model="newComment" placeholder="Kommentar hinzufügen"></textarea>
      <button type="submit">Kommentar hinzufügen</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, computed, capitalize } from 'vue'
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  ticketId: String,
})

const ticket = ref({
  id: '',
  ersteller_name: '',
  erstelldatum: '',
  kurs_name: '',
  kategorie: '',
  beschreibung: '',
  status: '',
  prioritaet: '',
  anhaenge: [],
  historie: [],
  kommentare: [],
})
const newComment = ref('')
const new_status = ref('')
const new_prioritaet = ref('')
const historieBeschreibung = ref('')
const userStore = useUserStore()

const loadTicketDetails = async () => {
  if (!props.ticketId) return
  const response = await fetch(`${API_URL}/ticket/getTicket/${props.ticketId}`)
  if (response.ok) {
    const data = await response.json()
    ticket.value = data
    console.log(data)
    new_status.value = data.status.toUpperCase()
    new_prioritaet.value = data.prioritaet.toUpperCase()
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
      status: new_status.value.toLowerCase(),
      prioritaet: (new_prioritaet.value || ticket.value.prioritaet)?.toLowerCase(),
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

const canEditTicket = computed(() => {
  return (
    (['dozent', 'tutor', 'admin'].includes(userStore.benutzer_rolle) &&
      ['neu', 'prüfung'].includes(ticket.value.status)) ||
    (['qm', 'admin'].includes(userStore.benutzer_rolle) && ticket.value.status === 'anpassung')
  )
})

const canSubmitComment = computed(() => {
  return !['geschlossen', 'abgelehnt'].includes(ticket.value.status)
})

const getPriorityClass = (priority) => {
  switch (priority.toUpperCase()) {
    case 'HOCH':
      return 'priority-high'
    case 'MITTEL':
      return 'priority-medium'
    case 'NIEDRIG':
      return 'priority-low'
    default:
      return ''
  }
}

const getStatusClass = (status) => {
  switch (status.toUpperCase()) {
    case 'NEU':
      return 'status-new'
    case 'PRÜFUNG':
      return 'status-review'
    case 'ANPASSUNG':
      return 'status-adjustment'
    case 'ABGELEHNT':
      return 'status-rejected'
    case 'GESCHLOSSEN':
      return 'status-closed'
    default:
      return ''
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
  line-height: 1.5;
}

p strong {
  color: #333;
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
  margin: 0px 8px;
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

.btn1 {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  text-transform: uppercase;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.priority-high {
  background-color: red;
  color: rgb(0, 0, 0);
}

.priority-medium {
  background-color: yellow;
  color: rgb(0, 0, 0);
}

.priority-low {
  background-color: lightgreen;
  color: rgb(0, 0, 0);
}

.status-new {
  background-color: lightblue;
  color: rgb(0, 0, 0);
}

.status-review {
  background-color: orange;
  color: rgb(0, 0, 0);
}

.status-adjustment {
  background-color: rgb(208, 0, 208);
  color: rgb(0, 0, 0);
}

.status-rejected {
  background-color: gray;
  color: rgb(0, 0, 0);
}

.status-closed {
  background-color: black;
  color: rgb(255, 255, 255);
}
</style>
