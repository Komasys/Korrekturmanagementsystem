<template>
  <div class="form-container">
    <h2>Ticket erstellen</h2>
    <p style="color: darkred; font-weight: 600">
      Wird noch erweitert u.a - Lernmaterial-Typ , Datei-upload
    </p>

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
        <select id="kurs_id" v-model="kurs_id" @change="loadLernmaterial" required>
          <option value="" disabled>Bitte Kurs wählen</option>
          <option v-for="kurs in kurse" :key="kurs.id" :value="kurs.id">
            {{ kurs.kuerzel }} - {{ kurs.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="lernmaterial">Lernmaterial:</label>
        <select id="lernmaterial" v-model="lernmaterial">
          <option value="" disabled>Bitte Lernmaterial wählen</option>
          <option v-for="lm in lernmaterialien" :key="lm.id" :value="lm.id">
            {{ lm.typ }}- {{ lm.titel }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="beschreibung">Beschreibung:</label>
        <textarea id="beschreibung" v-model="beschreibung" required></textarea>
      </div>

      <div class="form-group">
        <label for="file">Datei-Upload:</label>
        <input type="file" id="file" @change="handleFileUpload" accept="image/*,video/*" />
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
const lernmaterial = ref('')
const lernmaterialien = ref([])
const beschreibung = ref('')
const message = ref('')
const kurse = ref([])
const file = ref(null)

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

const loadLernmaterial = async () => {
  if (!kurs_id.value) return
  const response = await fetch(`${API_URL}/lernmaterial/getLernmaterial/${kurs_id.value}`)
  const data = await response.json()
  lernmaterialien.value = data
}

onMounted(() => {
  loadKategorien()
  loadKurse()
})

const handleFileUpload = (event) => {
  const uploadedFile = event.target.files[0]
  if (uploadedFile.size > 2 * 1024 * 1024) {
    alert('Die Datei darf nicht größer als 2MB sein.')
    file.value = null
    return
  }
  file.value = uploadedFile
}

const submitForm = async () => {
  const formData = new FormData()
  formData.append('kategorie', kategorie.value)
  formData.append('kurs_id', kurs_id.value)
  formData.append('lernmaterial_id', lernmaterial.value)
  formData.append('beschreibung', beschreibung.value)
  formData.append('benutzer_id', userStore.benutzer_id)
  if (file.value) {
    formData.append('file', file.value)
  }

  const response = await fetch(`${API_URL}/ticket/setTicket`, {
    method: 'POST',
    body: formData,
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
select,
input[type='file'] {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}
</style>
