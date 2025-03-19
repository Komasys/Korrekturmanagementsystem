<template>
  <div>
    <h1>Ticket Details</h1>
    <p style="color: darkred; font-weight: 600">
      Hier folgen noch Historie, Kommentare, Bearbeitungsfunktion, Statusändernungen, Kurs-ID zeigt
      dann nicht die Nummer sondern den Namen etc. pp
    </p>
    <p><strong>ID:</strong> {{ ticket.id }}</p>
    <p><strong>Beschreibung:</strong> {{ ticket.beschreibung }}</p>
    <p><strong>Kategorie:</strong> {{ ticket.kategorie }}</p>
    <p><strong>Kurs ID:</strong> {{ ticket.kurs_id }}</p>
    <p><strong>Ersteller ID:</strong> {{ ticket.ersteller_id }}</p>
    <p><strong>Erstellungsdatum:</strong> {{ new Date(ticket.erstelldatum).toLocaleString() }}</p>
    <!-- Weitere Ticket-Details hier -->
  </div>
  <h2>Diskussion</h2>
  <div></div>
</template>

<script setup>
import { ref, watch } from 'vue'
import API_URL from '@/api'

const props = defineProps({
  ticketId: String,
})

const ticket = ref({})

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

watch(() => props.ticketId, loadTicketDetails, { immediate: true })
</script>

<style scoped></style>
