<script setup>
import { useAuthStore } from '@/stores/auth.store';
import Profile from '@/components/Profile.vue';
import ChangePasswordButton from '@/components/buttons/ChangePasswordButton.vue';

const authStore = useAuthStore();
</script>

<template>
  <div class="profile">
    <h1 v-if="authStore.userInfo.is_active">Профиль</h1>
    <h1 class="blocked" v-else>Профиль заблокирован!</h1>
    <Profile />
    <ChangePasswordButton />
  </div>
</template>

<style scoped>
.profile {
  padding: 20px;
}

.profile h1 {
  margin-bottom: 20px;
}

.blocked, .emailCheck {
    color: brown;
}
</style>