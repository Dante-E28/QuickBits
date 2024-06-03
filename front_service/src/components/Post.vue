<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import PostService from '@/services/post.service';
import UserService from '@/services/user.service';

const posts = ref([]);
const users = ref({});

async function getPosts() {
    const postData = await PostService.getPosts();
    posts.value = postData.data;
    const userPromises = posts.value.map(post => UserService.getUser(post.user_id));
    const userDataArray = await Promise.all(userPromises);

    userDataArray.forEach((userData, index) => {
        if (userData) {
            users.value[posts.value[index].user_id] = userData.username;
        }
    });
}

onMounted(() => {
    getPosts();
});

const router = useRouter();

function goToPostDetail(postId) {
    router.push(`/post_detail/${postId}`);
}

function goToCreatePost() {
    router.push('/create_post');
}
</script>

<template>
  <div>
    <div v-for="post in posts" :key="post.id" class="post-container" @click="goToPostDetail(post.id)">
      <div class="post-header">
        <div class="author-info">
          <p class="author-name">{{ users[post.user_id] }}</p>
        </div>
        <button class="subscribe-button">Подписаться</button>
      </div>
      <h2 class="post-title">{{ post.name }}</h2>
      <p class="post-description">{{ post.description }}</p>
      <div class="post-actions">
        <span><i class="fas fa-heart"></i> {{ post.likes }}</span>
        <span><i class="fas fa-comment"></i> {{ post.comments }}</span>
        <span class="post-date">{{ new Date(post.date_create).toLocaleDateString() }}</span>
      </div>
    </div>
    <button class="floating-button" @click="goToCreatePost">Написать пост</button>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.post-container {
  max-width: 700px;
  margin: 30px auto;
  padding: 20px;
  color:#ffffff;
  background-color: #282c34;
  border-bottom: 3px solid #fc0909;
}

/* .post-container:hover {
  transform: scale(1.05);
} */

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-info {
  text-align: left;
}

.author-name {
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
  font-size: 14px;
  margin: 10px 0;
}

.post-description {
  font-size: 12px;
  margin: 10px 0;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
}

.post-actions i {
  margin-right: 5px;
}

.post-end h1 {
    font-size: 30px;
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
</style>