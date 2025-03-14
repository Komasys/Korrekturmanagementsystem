<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/signin">Sign In</RouterLink>
    <RouterLink to="/signup">Sign Up</RouterLink>
    <RouterLink to="/signout">Sign Out</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background-color: #f0f0f0;
}
</style>
