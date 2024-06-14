<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const authStore = useAuthStore();
const route = useRoute();
const errorShow = ref(null);
const response = ref(null);

async function verifyMe() {
    try {
        response.value = await authStore.verifyEmail(route.params.token);
    } catch(error) {
        errorShow.value = error;
    }
}

onMounted(async() => {
    await verifyMe();
});
</script>

<template>
  <div class="container">
    <h1 v-if="response">{{ response.message }}</h1>
    <h1 class="blocked" v-else>{{ errorShow }}</h1>
  </div>    
</template>

<style scoped>
.container {
  padding-top: 50px;
}

.blocked {
    color: brown;
}
</style>