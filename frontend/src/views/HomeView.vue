<template>
  <div>
    <h1>Home</h1>
    <p>Welcome to the Korrekturmanagementsystem!</p>
    <button @click="testCICD">Test CI/CD</button>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    testCICD() {
      alert('CI/CD is working!')
    },
  },
}
</script>

<style scoped>
button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #369870;
}
</style>
