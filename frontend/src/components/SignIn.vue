<template>
  <div class="container">
    <form @submit.prevent="signin" id="signinForm">
      <img src="@/assets/iu-logo-en-black-rgb-horizontal.png" alt="IU Logo" />
      <h1>Anmelden</h1>
      <input type="email" v-model="email" placeholder="Email" id="email" />
      <input type="password" v-model="password" placeholder="Password" id="password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import API_URL from '@/api'

const email = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const signin = async () => {
  const response = await fetch(`${API_URL}/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  })

  const result = await response.json()
  if (response.ok) {
    localStorage.setItem('access_token', result.access_token)
    router.push({ name: 'dashboard' })
  } else {
    message.value = result.message || 'Fehler bei der Anmeldung'
    alert(message.value)
  }
}
</script>

<style scoped>
img {
  height: 120px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

h1 {
  font-size: 1.5em;
  margin: -20px 0px 0px 0px;
}

p,
a {
  font-size: 14px;
  margin: 0px;
}
form {
  display: flex;
  flex-direction: column;
  text-align: center;
  gap: 10px;
  padding: 0px 20px 20px 20px;
  border: 1px solid #ccc;
  border-radius: 20px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

input,
button {
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 5px 10px;
  width: 100%;
  max-width: 400px;
  box-sizing: border-box;
  font-size: 16px;
}

button:hover {
  border: 1px solid rgb(66, 66, 66);
}
</style>
