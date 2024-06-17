<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { ref } from 'vue';
import PostService from '@/services/post.service';
import userService from '@/services/user.service';
import LikeService from '@/services/like.service';
import CommentService from '@/services/comment.service';

const user = ref(null);
const posts = ref(null);
const like = ref(null);

const authStore = useAuthStore();

async function test() {
    await authStore.refresh();
}

async function test2() {
    user.value = await userService.getMe();
}

async function testGetPosts() {
    posts.value = await PostService.getPosts();
}

async function testCreateLike() {
    await LikeService.createLike(1, '3a11e406-802e-4758-9465-8f9314c047c2')
}

async function testDeleteLike() {
    await LikeService.deleteLike(1, '3a11e406-802e-4758-9465-8f9314c047c2')
}

async function testGetLike() {
    like.value = await LikeService.getLike(3, '3a11e406-802e-4758-9465-8f9314c047c2')
}

async function submitComment() {
  const comment = {
    'post_id': 1,
    'text': content.value,
    'user_id': authStore.userInfo.id
  };
  await  CommentService.createComment(comment);
}

</script>

<template>
<div>
<button type="submit" @click="test">Рефреш</button>
<button type="submit" @click="test2">Юзер</button>
<button type="submit" @click="testGetPosts">Посты</button>
<button type="submit" @click="testCreateLike">Добавить</button>
<button type="submit" @click="testDeleteLike">Удалить</button>
<button type="submit" @click="testGetLike">Получить</button>

<p>{{ user }}</p>
<p>{{ posts }}</p>
<p>{{ like }}</p>
</div>
<div>
    <textarea id="content" v-model="content" required/>
    <button type="submit" @click.prevent="submitComment">Запостить</button>
</div>
</template>

<style scoped>

</style>