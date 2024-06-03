<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore()

const username = ref(null);
const password = ref(null);

async function handleLogin() {
  try {
    await authStore.login(username.value, password.value);
  } catch(error) {
    alert(error.response.data);
  }
}

</script>

<template>
    <form class="form-container">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" v-model="username">
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password">
      </div>
      <button type="submit" class="btn" @click.prevent="handleLogin">Войти</button>
    </form>
</template>

<style scoped>
.form-container {
  margin-top: 30px;
}

.form-control {
  margin-bottom: 20px;
}

.mb-3 {
    font-size: 18px;
}

.p {
  text-align: center;
}
</style>