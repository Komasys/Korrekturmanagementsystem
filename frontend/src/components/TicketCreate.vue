<template>
  <div class="form-container">
    <h2>Ticket erstellen</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="kategorie">Kategorie:</label>
        <select id="kategorie" v-model="kategorie" required>
          <option value="" disabled>Bitte Kategorie wählen</option>
          <option v-for="[unter, name] in Object.entries(kategorien)" :value="unter" :key="unter">
            {{ name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="kurs_id">Kurs:</label>
        <select id="kurs_id" v-model="kurs_id" required>
          <option value="" disabled>Bitte Kurs wählen</option>
          <option v-for="kurs in kurse" :key="kurs.id" :value="kurs.id">
            {{ kurs.kuerzel }} - {{ kurs.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="beschreibung">Beschreibung:</label>
        <textarea id="beschreibung" v-model="beschreibung" required></textarea>
      </div>

      <button type="submit">Absenden</button>
      <p v-if="message">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import API_URL from '@/api'

const kategorie = ref('')
const kategorien = ref({})
const kurs_id = ref('')
const beschreibung = ref('')
const message = ref('')
const kurse = ref([])

const userStore = useUserStore()

const loadKategorien = async () => {
  const response = await fetch(`${API_URL}/ticket/getTicketKategorien`)
  const data = await response.json()
  kategorien.value = data
}

const loadKurse = async () => {
  const response = await fetch(`${API_URL}/kurs/getKurse`)
  const data = await response.json()
  kurse.value = data
}

onMounted(() => {
  loadKategorien()
  loadKurse()
})

const submitForm = async () => {
  const response = await fetch(`${API_URL}/ticket/setTicket`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      kategorie: kategorie.value,
      kurs_id: kurs_id.value,
      beschreibung: beschreibung.value,
      benutzer_id: userStore.benutzer_id,
    }),
  })

  const result = await response.json()
  message.value = result.message || 'Fehler beim Erstellen des Tickets'
}
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
}

textarea,
select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}
</style>
