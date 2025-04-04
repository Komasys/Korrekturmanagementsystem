<template>
  <div v-if="!isStudent">
    <h1 class="titel">Bearbeitete Tickets</h1>
    <div class="filter-container">
      <label>
        <input type="checkbox" v-model="showClosedRejected" />
        Geschlossene und abgelehnte Tickets anzeigen
      </label>
      <div>
        <label for="filter">Filter:</label>
        <input id="filter" v-model="filterText" placeholder="Alles durchsuchen..." />
      </div>
    </div>
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
          <td class="status-cell">
            {{ ticket.status.charAt(0).toUpperCase() + ticket.status.slice(1) }}
          </td>
          <td class="datum-cell">
            {{
              new Date(ticket.erstelldatum).toLocaleDateString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
              })
            }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const tickets = ref([])
const router = useRouter()
const isStudent = computed(() => userStore.benutzer_rolle === 'student')

const showClosedRejected = ref(false)
const filterText = ref('')

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
    return (
      (showClosedRejected.value || !['abgelehnt', 'geschlossen'].includes(ticket.status)) &&
      (ticket.beschreibung.toLowerCase().includes(searchText) ||
        ticket.id.toLowerCase().includes(searchText) ||
        ticket.kategorie.toLowerCase().includes(searchText) ||
        ticket.status.toLowerCase().includes(searchText))
    )
  })
})

const loadBearbeiteteTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketsByBearbeiter/${userStore.benutzer_id}`)
  const data = await response.json()
  tickets.value = data
}

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
  loadBearbeiteteTickets()
})
</script>

<style scoped></style>
