<script setup>
import { ref } from 'vue';
import userService from '@/services/user.service';

const isChanging = ref(false);
const newPassword = ref(null);
const confirmPassword = ref(null);
const changeStatus = ref(null);

const changePassword = async () => {
  if(newPassword.value !== confirmPassword.value) {
    changeStatus.value = 'Пароли не совпадают.';
    return;
  }

  try {
    await userService.patchMe({'password': newPassword.value});
    changeStatus.value = 'Пароль успешно изменен.';
  } catch (error) {
    changeStatus.value = error;
  }
};
</script>

<template>
  <div>
    <button @click="isChanging = !isChanging" class="change-button">
      Изменить пароль
    </button>

    <div v-if="isChanging" class="change-password-form">
      <label>
        Новый пароль:
        <input type="password" v-model="newPassword" />
      </label>
      <label>
        Подтвердите новый пароль:
        <input type="password" v-model="confirmPassword" />
      </label>
      <button @click="changePassword" class="submit-button">
        Сохранить
      </button>
      <p v-if="changeStatus" class="status-message">{{ changeStatus }}</p>
    </div>
  </div>
</template>

<style scoped>
.change-password-form {
  margin-top: 20px;
}

.change-password-form label {
  display: block;
  margin-bottom: 10px;
}
</style>