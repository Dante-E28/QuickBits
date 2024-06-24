<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import PostService from '@/services/post.service';
import UserService from '@/services/user.service';
import LikeService from '@/services/like.service';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const currentUser = computed(() => authStore.userInfo);

const posts = ref([]);
const users = ref({});
const currentPage = ref(parseInt(route.query.page) || 1);
const postsPerPage = 5;

async function getPosts() {
    const postsData = await PostService.getPosts();
    posts.value = postsData;

    const postIds = posts.value.map(post => post.id);
    const likeData = await LikeService.getLikes(postIds);

    likeData.forEach((likes, index) => {
        if (likes) {
            posts.value[index].likes = likes.length;
        } else {
            posts.value[index].likes = 0;
        }
    });

    const userPromises = posts.value.map(post => UserService.getUser(post.user_id).catch(() => null));
    const userDataArray = await Promise.all(userPromises);

    userDataArray.forEach((userData, index) => {
        if (userData) {
            users.value[posts.value[index].user_id] = userData.username;
        } else {
            users.value[posts.value[index].user_id] = 'Олежка';
        }
    });
}

onMounted(() => {
    getPosts();
});

watch(currentPage, (newPage) => {
    router.push({ query: { ...route.query, page: newPage } });
});

const paginatedPosts = computed(() => {
    const start = (currentPage.value - 1) * postsPerPage;
    return posts.value.slice(start, start + postsPerPage);
});

function nextPage() {
    if ((currentPage.value * postsPerPage) < posts.value.length) {
        currentPage.value += 1;
    }
}

function previousPage() {
    if (currentPage.value > 1) {
        currentPage.value -= 1;
    }
}

function goToPostDetail(postId, authorName) {
    router.push({ name: 'PostDetailView', params: { postId }, query: { authorName } });
}

function goToCreatePost() {
    router.push('/create_post');
}

async function goToLikePost(postId, userId) {
    try {
        const existingLike = await LikeService.getLike(postId, userId);
        if (existingLike) {
            await LikeService.deleteLike(postId, userId);
            updatePostLikes(postId, false);
        } else {
            await LikeService.createLike(postId, userId);
            updatePostLikes(postId, true);
        }
    } catch (error) {
        console.error('Error liking post:', error);
    }
}

function updatePostLikes(postId, liked) {
    const post = posts.value.find(post => post.id === postId);
    if (post) {
        if (liked) {
            post.likes += 1;
        } else {
            post.likes -= 1;
        }
    }
}
</script>

<template>
  <div>
    <div v-for="post in paginatedPosts" :key="post.id" class="post-container" @click="goToPostDetail(post.id, users[post.user_id])">
      <div class="post-header">
          <p class="author-name">{{ users[post.user_id] }}</p>
      </div>
      <h2 class="post-title">{{ post.name }}</h2>
      <p class="post-description">{{ post.description }}</p>
      <div class="post-actions">
        <button class="like-button" @click.stop="goToLikePost(post.id, currentUser.id)">
          {{ post.likes }} ε(´｡•᎑•`)っ 💕
        </button>
        <span class="post-date">{{ new Date(post.date_create).toLocaleDateString() }}</span>
      </div>
    </div>
    <button class="floating-button" @click="goToCreatePost">Написать пост</button>
    <div class="pagination">
      <button @click="previousPage" :disabled="currentPage === 1">Предыдущая</button>
      <span>Страница {{ currentPage }}</span>
      <button @click="nextPage" :disabled="(currentPage * postsPerPage) >= posts.length">Следующая</button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.post-container {
  max-width: 700px;
  margin: 30px auto;
  padding: 20px;
  color: #ffffff;
  background-color: #282c34;
  border-bottom: 3px solid #fc0909;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-name {
  text-align: left;
  font-size: 12px;
  margin: 0;
}

.subscribe-button {
  background-color: #000;
  font-size: 10px;
  padding: 5px 7px !important;
  border: none;
  cursor: pointer;
  transition: transform 0.3s;
}

.subscribe-button:hover {
  transform: scale(1.1);
}

.post-title {
  font-size: 16px;
  margin: 10px 0;
}

.post-description {
  font-size: 14px;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 8; /* Показываем только 8 строк */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
  margin-right: 5px;
}

.like-button {
  background-color: white;
  border: 2px solid #ccc;
  border-radius: 15px;
  padding: 3px 6px; /* Уменьшены отступы внутри кнопки */
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.like-button:hover {
  border-color: #999; /* Изменение цвета границы при наведении */
}

.floating-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  font-family: 'Press Start 2P', cursive;
  font-size: 14px;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  transition: transform 0.3s;
}

.floating-button:hover {
  transform: scale(1.1);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 10px;
  padding: 10px 20px;
  cursor: pointer;
}

.pagination span {
  line-height: 40px;
}
</style>