<template>
  <div>
    <h1>Alle Tickets</h1>
    <p style="color: darkred; font-weight: 600">
      Zurzeit kann hier jeder alle Tickets sehen, später werden nur gewisse Rollen Zugriff haben.
    </p>
    <p style="color: darkgreen; font-weight: 600">
      Man kann auf die einzlnen Tickets klicken und kommt dann auf die Detailseite. Später wird man
      hier die Historie und das Ticket bearbeiten können.
    </p>
    <label>
      <input type="checkbox" v-model="showClosedTickets" /> Geschlossene Tickets anzeigen
    </label>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Beschreibung</th>
          <th>Kategorie</th>
          <th>Status</th>
        </tr>
        <tr>
          <th><input type="text" v-model="searchId" placeholder="Suche nach ID..." /></th>
          <th>
            <input
              type="text"
              v-model="searchBeschreibung"
              placeholder="Suche nach Beschreibung..."
            />
          </th>
          <th>
            <select v-model="searchKategorie">
              <option value="">Alle Kategorien</option>
              <option v-for="(label, value) in kategorien" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
          </th>
          <th>
            <select v-model="searchStatus">
              <option value="">Alle Status</option>
              <option v-for="(label, value) in status" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in filteredTickets" :key="ticket.id" @click="showDetails(ticket.id)">
          <td>{{ ticket.id }}</td>
          <td>{{ ticket.beschreibung }}</td>
          <td>{{ capitalize(ticket.kategorie) }}</td>
          <td>{{ capitalize(ticket.status) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import API_URL from '@/api'

const tickets = ref([])
const showClosedTickets = ref(false)
const searchId = ref('')
const searchBeschreibung = ref('')
const searchKategorie = ref('')
const searchStatus = ref('')
const kategorien = ref({})
const status = ref({})

const loadAllTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getAllTickets`)
  const data = await response.json()
  tickets.value = data
}

const loadKategorien = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketKategorien`)
  const data = await response.json()
  kategorien.value = data
}

const loadStatus = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketStatus`)
  const data = await response.json()
  status.value = data
}

const filteredTickets = computed(() => {
  return tickets.value
    .filter((ticket) => showClosedTickets.value || ticket.status !== 'geschlossen')
    .filter((ticket) => ticket.id.toString().includes(searchId.value))
    .filter((ticket) =>
      ticket.beschreibung.toLowerCase().includes(searchBeschreibung.value.toLowerCase()),
    )
    .filter(
      (ticket) =>
        !searchKategorie.value ||
        ticket.kategorie.toLowerCase() === searchKategorie.value.toLowerCase(),
    )
    .filter(
      (ticket) =>
        !searchStatus.value || ticket.status.toLowerCase() === searchStatus.value.toLowerCase(),
    )
})

const router = useRouter()

const showDetails = (ticketId) => {
  router.push({ name: 'ticket-details', params: { id: ticketId } })
}

const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

onMounted(() => {
  loadAllTickets()
  loadKategorien()
  loadStatus()
})
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}
</style>
