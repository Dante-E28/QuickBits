<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import PostService from '@/services/post.service';
import LikeService from '@/services/like.service';
import CommentService from '@/services/comment.service';

const route = useRoute();
const authStore = useAuthStore();

// Состояния
const post = ref(null);
const comments = ref([]);
const likeCount = ref();
const newComment = ref('');
const authorName = ref(route.query.authorName);
const currentUser = computed(() => authStore.userInfo);

async function getPost() {
    const postId = route.params.postId;
    post.value = await PostService.getPost(postId);
    await fetchLikes(postId);
}

async function fetchLikes(postId) {
  const likes = await LikeService.getLikes(postId);
  likeCount.value = likes.length;
};

async function submitComment() {
  const comment = {
    'post_id': post.value.id,
    'text': newComment.value,
    'user_id': authStore.userInfo.id
  };
  const createdComment = await CommentService.createComment(comment);
  comments.value.push({
    ...createdComment,
    expanded: false
  });
  newComment.value = '';
}

async function getComments() {
  const postId = route.params.postId;
  comments.value = await CommentService.getComments(postId)
  comments.value = comments.value.map(comment => ({
    ...comment,
    expanded: false
  }));
}

function toggleExpandComment(comment) {
  comment.expanded = !comment.expanded;
}

async function goToLikePost(postId, userId) {
    const existingLike = await LikeService.getLike(postId, userId);
    if (existingLike) {
        await LikeService.deleteLike(postId, userId);
    } else {
        await LikeService.createLike(postId, userId);
    }
    await fetchLikes(postId);
}

onMounted(() => {
    getPost();
    getComments();
});
</script>

<template>
  <div v-if="post" class="post-container">
    <div class="post-header">
      <p class="author-name">{{ authorName }}</p>
    </div>
      <h2 class="post-title">{{ post.name }}</h2>
      <p class="post-description">{{ post.description }}</p>
    <div class="post-actions">
        <button class="like-button" @click="goToLikePost(goToLikePost(post.id, currentUser.id))">
          {{ likeCount }} ε(´｡•᎑•`)っ 💕
        </button>
        <span class="post-date">{{ new Date(post.date_create).toLocaleDateString() }}</span>
    </div>
  </div>
  <div class="send-comment-container">
      <textarea id="newComment" v-model="newComment" class="comment-input" placeholder="Оставить комментарий"></textarea>
      <button @click="submitComment" class="comment-button">Кудасай</button>
  </div>
  <div v-for="comment in comments" :key="comment.id" class="comments-container">
    <div class="comments-header">
      <p class="author-name">{{ authorName }}</p>
    </div>
    <p v-if="comment.expanded" class="comments-description">{{ comment.text }}</p>
    <p v-else class="comments-description short">{{ comment.text }}</p>
    <button v-if="comment.text.split('\n').length > 8" @click="toggleExpandComment(comment)">
      {{ comment.expanded ? 'Скрыть' : 'Читать далее...' }}
    </button>
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

.send-comment-container {
  max-width: 700px;
  margin: 20px auto 0;
  position: relative;
}

.comment-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  resize: none;
}

.comment-button {
  padding: 10px 20px;
  background-color: #000;
  color: #000000;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.comment-button:hover {
  background-color: #333;
}

.comments-container {
  max-width: 700px;
  margin: 30px auto;
  padding: 20px;
  color: #ffffff;
  background-color: #282c34;
  border-bottom: 3px solid #fc0909;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comments-description {
  max-width: 700px;
  font-size: 13px;
  margin: 10px auto 0;
  position: relative;
}

.comments-description.short {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 8; /* показывать только 8 строк */
  -webkit-box-orient: vertical;
}
</style>