import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
    benutzer_id: '',
  }),
  actions: {
    setEmail(email) {
      this.email = email
    },
    setName(name) {
      this.name = name
    },
    setBenutzerId(benutzer_id) {
      this.benutzer_id = benutzer_id
    },
  },
})
