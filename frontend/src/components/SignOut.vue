<template>
  <button @click="signOut">Logout</button>
</template>

<script>
export default {
  methods: {
    signOut() {
      console.log('User signed out')
      localStorage.removeItem('access_token')
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
button {
  background-color: rgb(140, 0, 0);
  color: white;
  border: none;
  padding: 10px 10px;
  font-size: clamp(0.5rem, 2vw, 0.9rem);
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}
</style>
