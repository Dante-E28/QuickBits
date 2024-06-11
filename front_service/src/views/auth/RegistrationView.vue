<script setup>
import RegistrationForm from '@/components/auth/RegistrationForm.vue';
import { useAuthStore } from '@/stores/auth.store';
import SuccessRegistration from '@/components/auth/SuccessRegistration.vue';

const authStore = useAuthStore();

</script>

<template>
  <div class="container">
      <div v-if="!authStore.userInfo">
        <RegistrationForm />
      </div>
      <div v-else>
        <SuccessRegistration />
      </div>
  </div>    
</template>

<style scoped>
.container {
  padding-top: 50px;
}
</style>