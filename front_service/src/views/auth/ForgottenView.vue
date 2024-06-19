<script setup>
import { ref } from 'vue';
import { validateEmailInput } from '@/utils/validators';
import { useAuthStore } from '@/stores/auth.store';

const isSend = ref(null);
const email = ref(null);
const changeStatus = ref(null);

const authStore = useAuthStore();

function validateField() {
    changeStatus.value = validateEmailInput(email.value);
}

async function handleReset() {
    validateEmailInput();
    if (!changeStatus.value) {
        try {
            await authStore.sendEmailReset(email.value);
            isSend.value = !isSend.value;
        } catch(error) {
            changeStatus.value = error;
        }
    }
}
</script>

<template>
  <div class="container">
      <div v-if="!isSend">
        <h1>Сбросить на почту</h1>
        <form class="form-container">
            <div class="mb-3">
              <label for="email" class="form-label">Почта</label>
              <input type="text" class="form-control" id="email" v-model="email" @blur="validateField">
            </div>
            <button type="submit" @click.prevent="handleReset">Сбросить</button>
            <p v-if="changeStatus" class="status-message">{{ changeStatus }}</p>
        </form>
      </div>
      <div v-else>
        <h1>Отправлено на email!</h1>
      </div>
  </div>    
</template>

<style scoped>
.container {
  padding-top: 50px;
}

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

.error {
    margin-top: 10px;
    color: red;
}
</style>