<template>
  <nav>
    <button @click="toggleTicketCreate">Ticket erstellen</button>
    <button @click="toggleMyTickets">Meine Tickets</button>
    <RouterLink to="/"><SignOut /></RouterLink>
  </nav>
  <main>
    <TicketCreate v-if="showTicketCreate" />
    <MyTickets v-if="showMyTickets" />
  </main>
</template>

<script setup>
import { ref } from 'vue'
import SignOut from '@/components/SignOut.vue'
import TicketCreate from '@/components/TicketCreate.vue'
import MyTickets from '@/components/MyTickets.vue'

const showTicketCreate = ref(false)
const showMyTickets = ref(false)

const toggleTicketCreate = () => {
  showTicketCreate.value = !showTicketCreate.value
  if (showTicketCreate.value) {
    showMyTickets.value = false
  }
}

const toggleMyTickets = () => {
  showMyTickets.value = !showMyTickets.value
  if (showMyTickets.value) {
    showTicketCreate.value = false
  }
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #f0f0f0;
  align-items: center;
}

a,
button {
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

p {
  margin: 0px;
  font-size: 20px;
}
</style>
