<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import CommentService from '@/services/comment.service';
import UserService from '@/services/user.service';

const props = defineProps({
    postId: {
        type: Number,
        required: true
    }
});
const authStore = useAuthStore();

// Состояния
const comments = ref([]);
const newComment = ref('');
const editComment = ref(null);
const editText = ref('');
const currentUser = computed(() => authStore.userInfo);

async function getComments() {
    const fetchedComments = await CommentService.getComments(props.postId);
    comments.value = await Promise.all(fetchedComments.map(async comment => {
        const user = await UserService.getUser(comment.user_id);
        return {
            ...comment,
            user,
            expanded: false
        };
    }));
}

async function submitComment() {
    const comment = {
        'post_id': props.postId,
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

function toggleExpandComment(comment) {
    comment.expanded = !comment.expanded;
}

async function deleteComment(commentId) {
    await CommentService.deleteComment(commentId);
    comments.value = comments.value.filter(comment => comment.id !== commentId);
}

function startUpdateComment(comment) {
    editComment.value = comment;
    editText.value = comment.text;
}

async function updateComment(userId) {
    await CommentService.updateComment(editComment.value.id, editText.value, userId);
    editComment.value = null;
    editText.value = '';
    await getComments();
}

function cancelUpdateComment() {
    editComment.value = null;
    editText.value = '';
}

onMounted(() => {
    getComments();
});
</script>

<template>
    <div class="send-comment-container">
        <textarea id="newComment" v-model="newComment" class="comment-input" placeholder="Оставить комментарий"></textarea>
        <button @click="submitComment" class="comment-button">Кудасай</button>
    </div>

    <div v-for="comment in comments" :key="comment.id" class="comments-container">
        <div class="comment-header">
            <p class="author-name">{{ comment.user.username }}</p>
        </div>
        <div v-if="editComment && editComment.id === comment.id">
            <textarea v-model="editText" class="comment-input"></textarea>
            <button @click="updateComment(currentUser.id)" class="comment-button">Сохранить</button>
            <button @click="cancelUpdateComment" class="comment-button">Отменить</button>
        </div>
        <div v-else>
            <p v-if="comment.expanded" class="comments-description">{{ comment.text }}</p>
            <p v-else class="comments-description short">{{ comment.text }}</p>
            <button v-if="comment.text.split('\n').length > 8" @click="toggleExpandComment(comment)">
                {{ comment.expanded ? 'Скрыть' : 'Читать далее...' }}
            </button>
        </div>
        <button v-if="comment.user_id === currentUser.id" @click="deleteComment(comment.id)">Удалить</button>
        <button v-if="comment.user_id === currentUser.id" @click="startUpdateComment(comment)">Редактировать</button>
    </div>
</template>

<style scoped>
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