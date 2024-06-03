<script setup>
import { useAuthStore } from '@/stores/auth.store';
import AuthService from '@/services/auth.service';
import { ref } from 'vue';
import PostService from '@/services/post.service';

const user = ref(null);
const posts = ref(null);

const authStore = useAuthStore();

async function test() {
    await authStore.refresh();
}

async function test2() {
    user.value = await AuthService.fetchUser();
}

async function testGetPosts() {
    const postData = await PostService.getPosts();
    posts.value = postData.data;
}

</script>

<template>
<button type="submit" @click="test">Рефреш</button>
<button type="submit" @click="test2">Юзер</button>
<button type="submit" @click="testGetPosts">Посты</button>
<p>{{ user }}</p>
<p>{{ posts }}</p>
</template>

<style scoped>

</style>