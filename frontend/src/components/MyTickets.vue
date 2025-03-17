<template>
  <div>
    <h1>Meine Tickets</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Beschreibung</th>
          <th>Kategorie</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.id">
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
import API_URL from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const tickets = ref([])

const loadAllTickets = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketsByUser/${userStore.benutzer_id}`)
  const data = await response.json()
  tickets.value = data
}
onMounted(() => {
  loadAllTickets()
})
</script>

<style scoped></style>
