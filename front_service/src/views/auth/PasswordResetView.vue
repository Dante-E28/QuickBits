<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const authStore = useAuthStore();
const route = useRoute();
const errorShow = ref(null);
const response = ref(null);

const password = ref(null);
const confirmPassword = ref(null);

async function handleReset() {
    if (password.value !== confirmPassword.value) {
        errorShow.value = 'Пароли не совпадают!';
    } else {
        try {
            response.value = await authStore.resetPassword(route.params.token, password.value);
        } catch(error) {
            errorShow.value = error;
        }
    }
}
</script>

<template>
  <div class="container">
    <form class="form-container" v-if="!response">
      <div class="mb-3">
        <label for="password" class="form-label">Новый пароль</label>
        <input type="password" class="form-control" id="password" v-model="password">
      </div>
      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Подтвердите пароль</label>
        <input type="password" class="form-control" id="password" v-model="confirmPassword">
      </div>
      <button type="submit" @click.prevent="handleReset">Сбросить</button>
      <p v-if="errorShow" class="error-message">{{ errorShow }}</p>
    </form>
    <h1 v-else>{{ response.message }}</h1>
  </div>    
</template>

<style scoped>
.container {
  padding-top: 50px;
}

.error-message {
  margin-top: 10px;
  color: brown;
}
</style>