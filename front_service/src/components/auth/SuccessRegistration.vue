<script setup>
import SuccessLogin from '@/components/auth/SuccessLogin.vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore();

</script>

<template>
<SuccessLogin />
<h1 v-if="!authStore.userInfo.is_verified">Подтверди email!</h1>
</template>

<style scoped>

</style>