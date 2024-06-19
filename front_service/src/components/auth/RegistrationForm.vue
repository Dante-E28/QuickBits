<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import { validateEmailInput, validatePasswordInput, validateUsernameInput } from '@/utils/validators';

const authStore = useAuthStore()

const username = ref(null);
const password = ref(null);
const email = ref(null);
const confirmPassword = ref(null);

const changeStatus = ref(null);
const usernameError = ref(null);
const passwordError = ref(null);
const emailError = ref(null);

function validateFields() {
    usernameError.value = validateUsernameInput(username.value);
    passwordError.value = validatePasswordInput(password.value);
    emailError.value = validateEmailInput(email.value);
}

async function handleReg() {
    validateFields();
    if (!usernameError.value && !passwordError.value && !emailError.value) {
        if (password.value !== confirmPassword.value) {
            changeStatus.value = 'Пароли не совпали!'
        } else {
            try {
                await authStore.register(username.value, email.value, password.value);
            } catch(error) {
                changeStatus.value = error;
            }
        }
    }
}

</script>

<template>
    <form class="form-container">
      <div class="mb-3">
        <label for="username" class="form-label">Юзернейм</label>
        <input type="text" class="form-control" id="username" v-model="username">
      </div>
      <p v-if="usernameError" class="status-message">{{ usernameError }}</p>
      <div class="mb-3">
        <label for="email" class="form-label">Е-мейл</label>
        <input type="text" class="form-control" id="email" v-model="email">
      </div>
      <p v-if="emailError" class="status-message">{{ emailError }}</p>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль</label>
        <input type="password" class="form-control" id="password" v-model="password">
      </div>
      <p v-if="passwordError" class="status-message">{{ passwordError }}</p>
      <div class="mb-3">
        <label for="password" class="form-label">Еще раз</label>
        <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword">
      </div>
      <button type="submit" @click.prevent="handleReg">Welcome</button>
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

.reg {
  font-size: 13px !important;
}
</style>