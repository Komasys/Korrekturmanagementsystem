<template>
  <nav>
    <div class="ticket-links">
      <RouterLink to="/dashboard/create-ticket" v-if="!isQM">Ticket erstellen</RouterLink>
      <RouterLink to="/dashboard/my-tickets" v-if="!isQM">Meine Tickets</RouterLink>
      <RouterLink to="/dashboard/bearbeitete-tickets" v-if="!isStudent"
        >Bearbeitete Tickets</RouterLink
      >
      <RouterLink to="/dashboard/all-tickets" v-if="!isStudent">Alle Tickets</RouterLink>
    </div>
    <div class="sign-out">
      <SignOut />
    </div>
  </nav>
  <main>
    <RouterView />
  </main>
  <footer>
    <p>Rolle: {{ userStore.benutzer_rolle }}</p>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import SignOut from '@/components/SignOut.vue'
const userStore = useUserStore()
const isStudent = computed(() => userStore.benutzer_rolle === 'student')
const isQM = computed(() => ['qm'].includes(userStore.benutzer_rolle))
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #f0f0f0;
  align-items: center;
}

.ticket-links {
  display: flex;
  width: 100%;
  justify-content: space-around;
}

a {
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  color: black;
}

p {
  margin: 0px;
  font-size: 20px;
}

footer {
  padding: 10px;
  background-color: #f0f0f0;
  text-align: center;
  position: fixed;
  bottom: 0;
  right: 0;
}
</style>
