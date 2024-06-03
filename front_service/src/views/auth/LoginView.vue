<script setup>
import LoginForm from '@/components/auth/LoginForm.vue';
import { useAuthStore } from '@/stores/auth.store';
import SuccessLogin from '@/components/auth/SuccessLogin.vue';

const authStore = useAuthStore();

</script>

<template>
  <div class="container">
      <div v-if="!authStore.userInfo">
        <LoginForm />
      </div>
      <div v-else>
        <SuccessLogin />
      </div>
  </div>    
</template>

<style scoped>
.container {
  padding-top: 50px;
}
</style>