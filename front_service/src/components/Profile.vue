<script setup>
import { patchMeLogoutToLogin } from '@/services/requestHelper';
import { useAuthStore } from '@/stores/auth.store';
import { ref } from 'vue';

const authStore = useAuthStore();
const isEditing = ref(false);
const editedUser = ref({});
const errorShow = ref(null);

async function toggleEditMode() {
    errorShow.value = null;
    if (isEditing.value) {
        try {
            const username = editedUser.value.username;
            const email = editedUser.value.email;
            await patchMeLogoutToLogin(username, email);
        } catch(error) {
            console.error('Edit user failed: ', error);
            errorShow.value = error;
        }
    } else {
        editedUser.value = { ...authStore.userInfo };
    }
    isEditing.value = !isEditing.value;
}
</script>

<template>
    <div v-if="authStore.userInfo">
      <div class="mb-3">
        <label>Имя:</label>
        <span v-if="!isEditing">{{ authStore.userInfo.username }}</span>
        <input v-else v-model="editedUser.username" />
      </div>
      <div class="mb-3">
        <label>Email:</label>
        <span v-if="!isEditing">{{ authStore.userInfo.email }}</span>
        <input v-else v-model="editedUser.email" />
      </div>
      <h1 v-if="errorShow"> {{ errorShow }}</h1>
      <button class="mb-3" @click="toggleEditMode">
        {{ isEditing ? 'Сохранить' : 'Редактировать' }}
      </button>
    </div>
    <div v-else>
      <p>Загрузка данных профиля...</p>
    </div>
</template>

<style scoped>
label {
  display: inline-block;
  width: 100px;
}

input {
  margin-bottom: 10px;
}
</style>