<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore()

const username = ref('');
const password = ref('');

async function handleLogin() {
    try {
      await authStore.login(username.value, password.value);
    } catch(error) {
      console.log('Login failed: ', error);
    }
    
}

</script>

<template>
<div class="container">
    <form class="form-container" v-if="!authStore.userInfo">
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
    <pre v-else class="ascii-art">
        
        ───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───
        ───█▒▒░░░░░░░░░▒▒█───
        ────█░░█░░░░░█░░█────
        ─▄▄──█░░░▀█▀░░░█──▄▄─
        █░░█─▀▄░░░░░░░▄▀─█░░█
        █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
        █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
        █░░║║║╠─║─║─║║║║║╠─░░█
        █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
        █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
      </pre>
</div>    
</template>

<style scoped>
.container {
  padding-top: 50px; /* Увеличиваем отступ сверху */
}

.form-container {
  margin-top: 30px; /* Увеличиваем отступ между заголовком и формой */
}

.form-control {
  margin-bottom: 20px; /* Отступы между строками ввода */
}

.mb-3 {
    font-size: 18px;
}

.p {
  text-align: center;
}

.ascii-art {
  font-family: 'Courier New', Courier, monospace;
  text-align: center;
  white-space: pre;
  line-height: 1.2;
}
</style>