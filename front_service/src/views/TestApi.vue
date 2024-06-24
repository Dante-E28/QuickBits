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
const likes = ref(null);

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
    'post_id': 2,
    'text': '1111выфв11',
    'user_id': '37a7f82b-6338-4885-af9e-d76ba733aa10'
  };
  await CommentService.createComment(comment);
}

async function deleteComment() {
    await CommentService.deleteComment(14)
}

async function updateComment() {
    await CommentService.updateComment(25, 'Эшкере!', '3a11e406-802e-4758-9465-8f9314c047c2'
    )
} 

async function testGetLikes() {
    const response = await LikeService.getLikes([10, 11]);
    likes.value = response.data;
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
<button type="submit" @click="testGetLikes">Получить лайки постов 10 и 11</button>

<p>{{ user }}</p>
<p>{{ posts }}</p>
<p>{{ likes }}</p>
</div>
<div>
    <button type="submit" @click.prevent="submitComment">Запостить</button>
    <button type="submit" @click.prevent="deleteComment">Удалить</button>
    <button type="submit" @click.prevent="updateComment">Обновить</button>
</div>
</template>

<style scoped>

</style>