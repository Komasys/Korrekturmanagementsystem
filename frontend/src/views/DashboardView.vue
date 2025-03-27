<template>
  <nav>
    <div class="ticket-links">
      <RouterLink to="/dashboard/create-ticket" v-if="!isQM">Ticket erstellen</RouterLink>
      <RouterLink to="/dashboard/my-tickets" v-if="!isQM">Meine Tickets</RouterLink>
      <RouterLink to="/dashboard/bearbeitete-tickets" v-if="!isStudent"
        >Bearbeitete Tickets</RouterLink
      >
      <RouterLink to="/dashboard/all-tickets" v-if="!isStudent">Alle Tickets</RouterLink>
      <SignOut />
    </div>
  </nav>
  <main>
    <RouterView />
  </main>
  <footer>
    <button
      class="help"
      onclick="window.open('/benutzerhandbuch', '_blank')"
      title="Benutzerhandbuch"
    >
      ?
    </button>
    <p class="role">Rolle: {{ userStore.benutzer_rolle }}</p>
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
  padding: 10px;
  background-color: #f0f0f0;
  align-items: center;
}

.ticket-links {
  display: flex;
  width: 100%;
  justify-content: space-around;
  align-items: center;
  gap: 20px;
}

a {
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: clamp(0.7rem, 2vw, 1.25rem);
  font-weight: bold;
  color: black;
}

p {
  margin: 0px;
  font-size: 20px;
}

.role {
  padding: 10px;
  background-color: #f0f0f0;
  text-align: center;
  position: fixed;
  bottom: 0;
  right: 0;
}

.help {
  position: fixed;
  bottom: 0;
  left: 0;
  background-color: #14dcc1;
  border: none;
  border-radius: 50%;
  font-weight: 700;
  cursor: pointer;
  padding: 10px;
  margin: 10px;
  width: 40px;
  height: 40px;
  color: rgb(255, 255, 255);
  font-size: 20px;
}

.help:hover {
  background-color: #3b6e67;
}
</style>
