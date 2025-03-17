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
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Beschreibung</th>
          <th>Kategorie</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.id" @click="showDetails(ticket.id)">
          <td>{{ ticket.id }}</td>
          <td>{{ ticket.beschreibung }}</td>
          <td>{{ ticket.kategorie }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import API_URL from '@/api'

const tickets = ref([])

const loadAllTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getAllTickets`)
  const data = await response.json()
  tickets.value = data
}

const router = useRouter()

const showDetails = (ticketId) => {
  router.push({ name: 'ticket-details', params: { id: ticketId } })
}

onMounted(() => {
  loadAllTickets()
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
