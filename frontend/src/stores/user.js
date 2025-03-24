import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    email: '',
    benutzer_id: '',
    benutzer_rolle: '',
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
    setBenutzerRolle(benutzer_rolle) {
      this.benutzer_rolle = benutzer_rolle
    },
  },
})
