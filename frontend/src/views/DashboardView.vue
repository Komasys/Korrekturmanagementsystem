<template>
  <nav>
    <RouterLink to="/dashboard/create-ticket">Ticket erstellen</RouterLink>
    <RouterLink to="/dashboard/my-tickets">Meine Tickets</RouterLink>
    <RouterLink to="/dashboard/all-tickets">Alle Tickets</RouterLink>
    <SignOut />
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<script setup>
import SignOut from '@/components/SignOut.vue'
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #f0f0f0;
  align-items: center;
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
</style>
