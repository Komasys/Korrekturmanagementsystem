<template>
  <div class="container">
    <button @click="signOut">Logout</button>
  </div>
</template>

<script>
export default {
  methods: {
    signOut() {
      console.log('User signed out');
      localStorage.removeItem('access_token');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: end;
  padding-top: 20px;
}

button {
  padding: 10px;
  font-size: 14px;
  border: 1px solid rgb(205, 205, 205);
  border-radius: 10px;
}
</style>
