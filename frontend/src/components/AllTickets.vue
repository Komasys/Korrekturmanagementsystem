<template>
  <div v-if="!isStudent">
    <h1 class="titel">Alle Tickets</h1>
    <div class="filter-container">
      <div class="filter-options">
        <label>
          <input type="checkbox" v-model="showClosedRejected" /> Geschlossene und abgelehnte Tickets
          anzeigen
        </label>
        <label>
          <input type="checkbox" v-model="showMyKursTickets" /> Meine Kurstickets anzeigen
        </label>
      </div>
      <div class="filter-search">
        <label for="filter">Filter:</label>
        <input id="filter" v-model="filterText" placeholder="Alles durchsuchen..." />
      </div>
    </div>
    <div class="table-responsive">
      <table>
        <thead>
          <tr>
            <th class="status_th"></th>
            <th class="id-cell" @click="sortTable('id')">
              ID <span>{{ getSortIcon('id') }}</span>
            </th>
            <th class="cell beschreibung-cell" @click="sortTable('beschreibung')">
              Beschreibung <span>{{ getSortIcon('beschreibung') }}</span>
            </th>
            <th class="cell kategorie-cell" @click="sortTable('kategorie')">
              Kategorie <span>{{ getSortIcon('kategorie') }}</span>
            </th>
            <th class="status-cell" @click="sortTable('status')">
              Status <span>{{ getSortIcon('status') }}</span>
            </th>
            <th class="datum-cell" @click="sortTable('erstelldatum')">
              Datum <span>{{ getSortIcon('erstelldatum') }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in filteredTickets" :key="ticket.id" @click="showDetails(ticket.id)">
            <td class="priority-bar" :class="getPriorityClass(ticket.prioritaet)"></td>
            <td class="cell id-cell">{{ ticket.id }}</td>
            <td class="cell beschreibung-cell">{{ ticket.beschreibung }}</td>
            <td class="cell kategorie-cell">
              {{ ticket.kategorie.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase()) }}
            </td>
            <td class="cell status-cell">
              {{ ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1) }}
            </td>
            <td class="datum-cell">
              <time :datetime="ticket.erstelldatum">{{
                new Date(ticket.erstelldatum).toLocaleDateString()
              }}</time>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'

const tickets = ref([])
const kursTickets = ref([])
const showClosedRejected = ref(false)
const showMyKursTickets = ref(false)
const filterText = ref('')
const kategorien = ref({})
const status = ref({})
const userStore = useUserStore()

const isStudent = computed(() => userStore.benutzer_rolle === 'student')

const allowedStatus = {
  student: [],
  dozent: ['neu', 'prüfung', 'abgelehnt', 'geschlossen'],
  tutor: ['neu', 'prüfung', 'abgelehnt', 'geschlossen'],
  qm: ['anpassung', 'abgelehnt', 'geschlossen'],
  admin: ['neu', 'abgelehnt', 'prüfung', 'anpassung', 'geschlossen'],
}

const loadAllTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getAllTickets`)
  const data = await response.json()
  tickets.value = data
}

const loadKursTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getKursTicketsByUser/${userStore.benutzer_id}`)
  const data = await response.json()
  kursTickets.value = data
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

const sortKey = ref('')
const sortOrder = ref(1)

const sortTable = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = -sortOrder.value
  } else {
    sortKey.value = key
    sortOrder.value = 1
  }
}

const getSortIcon = (key) => {
  if (sortKey.value === key) {
    return sortOrder.value === 1 ? '▲' : '▼'
  }
  return ''
}

const filteredTickets = computed(() => {
  const sortedTickets = [...tickets.value].sort((a, b) => {
    if (a[sortKey.value] < b[sortKey.value]) return -1 * sortOrder.value
    if (a[sortKey.value] > b[sortKey.value]) return 1 * sortOrder.value
    return 0
  })
  return sortedTickets.filter((ticket) => {
    const searchText = filterText.value.toLowerCase()
    const isKursTicket = showMyKursTickets.value
      ? kursTickets.value.some((kursTicket) => kursTicket.id === ticket.id)
      : true
    const isAllowedStatus = allowedStatus[userStore.benutzer_rolle].includes(
      ticket.status.toLowerCase(),
    )
    return (
      isKursTicket &&
      isAllowedStatus &&
      (showClosedRejected.value || !['abgelehnt', 'geschlossen'].includes(ticket.status)) &&
      (ticket.beschreibung.toLowerCase().includes(searchText) ||
        ticket.id.toLowerCase().includes(searchText) ||
        ticket.kategorie.toLowerCase().includes(searchText) ||
        ticket.status.toLowerCase().includes(searchText))
    )
  })
})

const router = useRouter()

const showDetails = (ticketId) => {
  router.push({ name: 'ticket-details', params: { id: ticketId } })
}

const getPriorityClass = (priority) => {
  switch (priority?.toUpperCase()) {
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

onMounted(() => {
  loadAllTickets()
  loadKursTickets()
  loadKategorien()
  loadStatus()
})
</script>

<style scoped></style>
