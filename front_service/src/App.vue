<script setup>
import Navbar from './components/Navbar.vue'
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth.store';

const authStore = useAuthStore();

onMounted(async () => {
    await authStore.checkAuth();
});
</script>

<template>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    </head>
    <Navbar />
    <RouterView />
</template>

<style scoped>

</style>
