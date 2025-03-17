<template>
  <div>
    <h1>Meine Tickets</h1>
    <p style="color: darkred; font-weight: 600">
      Hier werden nur selbst erstellten Tickets angezeigt.
    </p>
    <p style="color: darkgoldenrod; font-weight: 600">Spalten sind nicht final.</p>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Beschreibung</th>
          <th>Kategorie</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.id">
          <td>{{ ticket.id }}</td>
          <td>{{ ticket.beschreibung }}</td>
          <td>{{ ticket.kategorie }}</td>
          <td style="color: darkgoldenrod">coming soon</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const tickets = ref([])

const loadAllUserTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketsByUser/${userStore.benutzer_id}`)
  const data = await response.json()
  tickets.value = data
}
onMounted(() => {
  loadAllUserTickets()
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
