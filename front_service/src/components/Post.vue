<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import PostService from '@/services/post.service';
import LikeService from '@/services/like.service';
import Comments from './Comments.vue';

const route = useRoute();
const authStore = useAuthStore();

// Состояния
const post = ref(null);
const likeCount = ref(0);
const editPost = ref(null);
const editName = ref('');
const editDescription = ref('');
const authorName = ref(route.query.authorName);
const currentUser = computed(() => authStore.userInfo);

async function getPost() {
    const postId = route.params.postId;
    post.value = await PostService.getPost(postId);
    await fetchLikes([postId]);
}

async function fetchLikes(postIds) {
    const likes = await LikeService.getLikesCount(postIds);
    if (likes && likes.length) {
        likeCount.value = likes[0];
    }
}

async function goToLikePost(postId, userId) {
    const existingLike = await LikeService.getLike(postId, userId);
    if (existingLike) {
        await LikeService.deleteLike(postId, userId);
    } else {
        await LikeService.createLike(postId, userId);
    }
    await fetchLikes([postId]);
}

function startEditPost(post) {
    if (currentUser.value.is_superuser || post.user_id === currentUser.value.id) {
        editPost.value = post;
        editName.value = post.name;
        editDescription.value = post.description;
    }
}

async function updatePost() {
    if (editPost.value) {
        await PostService.updatePost(editPost.value.id, editName.value, editDescription.value);
        editPost.value = null;
        await getPost();
    }
}

async function deletePost(postId) {
    if (currentUser.value.is_superuser || post.value.user_id === currentUser.value.id) {
        await PostService.deletePost(postId);
        post.value = null;
    }
}

function cancelEditPost() {
    editPost.value = null;
    editName.value = '';
    editDescription.value = '';
}

onMounted(() => {
    getPost();
});
</script>

<template>
    <div v-if="post" class="post-container">
        <div class="post-header">
            <p class="author-name">{{ authorName }}</p>
        </div>

        <div v-if="editPost">
            <input v-model="editName" class="post-title-input" placeholder="Название поста" />
            <textarea v-model="editDescription" class="post-description-input" placeholder="Описание поста"></textarea>
            <div class="post-actions">
                <button @click="updatePost" class="save-button">Сохранить</button>
                <button @click="cancelEditPost" class="cancel-button">Отменить</button>
            </div>
        </div>

        <div v-else>
            <h2 class="post-title">{{ post.name }}</h2>
            <p class="post-description">{{ post.description }}</p>
            <div class="post-actions">
                <button v-if="currentUser.is_superuser || post.user_id === currentUser.id" @click="startEditPost(post)" class="edit-button">Редактировать пост</button>
                <button v-if="currentUser.is_superuser || post.user_id === currentUser.id" @click="deletePost(post.id)" class="delete-button">Удалить пост</button>
                <button class="like-button" @click="goToLikePost(post.id, currentUser.id)">
                    {{ likeCount }} ε(´｡•᎑•`)っ 💕
                </button>
                <span class="post-date">{{ new Date(post.date_create).toLocaleDateString() }}</span>
            </div>
        </div>
    </div>
    
    <Comments :postId="post.id" />
</template>

<style scoped>
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

.post-title-input,
.post-description-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 8px;
}

.save-button,
.cancel-button {
    background-color: #007BFF;
    color: rgb(0, 0, 0);
    border: none;
    padding: 8px 16px;
    cursor: pointer;
}

.save-button:hover,
.cancel-button:hover {
    background-color: #0056b3;
}
</style>