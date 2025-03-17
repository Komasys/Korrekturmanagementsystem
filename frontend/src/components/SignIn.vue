<template>
  <div class="container">
    <form @submit.prevent="signin" id="signinForm">
      <h1>Anmelden</h1>
      <input type="email" v-model="email" placeholder="Email" id="email" />
      <input type="password" v-model="password" placeholder="Password" id="password" />
      <button type="submit">Login</button>
      <p>Noch kein Konto?</p>
      <a href="/signup">Hier registrieren</a>
      <br />
      <p style="color: darkred; font-weight: 600">
        Registrierung wird es später natürlich nicht geben. Testzweck only
      </p>
      <p style="max-width: 400px">
        Es gibt im System noch keine GUI-Fehlermeldung, Infos zu Fehlern finden sich in der
        Entwicklungsconsole (F12 (Chrome, Firefox, Edge) oder Strg+Shift+I (Windows) bzw.
        Cmd+Option+I (Mac))
      </p>
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
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

h1 {
  font-size: 2em;
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
  padding: 20px;
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
