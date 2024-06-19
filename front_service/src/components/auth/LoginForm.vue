<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import { validatePasswordInput, validateUsernameInput } from '@/utils/validators';

const authStore = useAuthStore()

const username = ref(null);
const password = ref(null);

const changeStatus = ref(null);
const passwordError = ref(null);
const usernameError = ref(null);

function validateFields() {
    usernameError.value = validateUsernameInput(username.value);
    passwordError.value = validatePasswordInput(password.value);
}

async function handleLogin() {
    validateFields();
    if (!usernameError.value && !passwordError.value) {
        try {
          await authStore.login(username.value, password.value);
        } catch(error) {
          changeStatus.value = error;
        }
    }
}

</script>

<template>
    <form class="form-container">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" v-model="username">
      </div>
      <p v-if="usernameError" class="status-message">{{ usernameError }}</p>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password">
      </div>
      <p v-if="passwordError" class="status-message">{{ passwordError }}</p>
      <button type="submit" @click.prevent="handleLogin">Войти</button>
      <router-link class="nav-link reg" to="/registration">регнуть?</router-link>
      <router-link class="nav-link forget" to="/forgotten">забыл?</router-link>
      <p v-if="changeStatus" class="status-message">{{ changeStatus }}</p>
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

.reg, .forget {
  font-size: 13px !important;
}
</style>