<template>
  <form @submit.prevent="signup" id="signupForm">
    <input type="text" v-model="name" placeholder="Name" id="name" />
    <input type="email" v-model="email" placeholder="E-Mail" id="email" />
    <input type="password" v-model="password" placeholder="Passwort" id="password" />
    <button type="submit">Registrieren</button>
  </form>
  <p id="message">{{ message }}</p>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')
const message = ref('')

const signup = async () => {
  const response = await fetch('http://localhost:5000/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: name.value,
      email: email.value,
      password: password.value,
    }),
  })

  const result = await response.json()
  message.value = result.message || 'Fehler bei der Registrierung'
}
</script>
