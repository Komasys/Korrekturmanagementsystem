<template>
  <SignIn />
  <footer>
    <button
      class="help"
      onclick="window.open('/benutzerhandbuch', '_blank')"
      title="Benutzerhandbuch"
    >
      ?
    </button>
  </footer>
</template>

<script>
import SignIn from '@/components/SignIn.vue'

export default {
  components: {
    SignIn,
  },
}
</script>

<style scoped>
.help {
  position: fixed;
  bottom: 0;
  left: 0;
  background-color: #48906a;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 10px;
  margin: 10px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgb(234, 234, 234);
}

.help:hover {
  background-color: #3b6e4d;
}
</style>
