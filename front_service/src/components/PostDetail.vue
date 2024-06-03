<script setup>
import { ref } from 'vue';
const post = ref({
    title: 'Заголовок',
    description: 'Тело статьи',
    author: {
        name: 'Имя автора'
    },
    likes: 'Количество лайков',
    comments: 'количество комментов'
})

</script>

<template>
  <div class="post-detail-container">
    <h1 class="post-title">{{ post.title }}</h1>
    <p class="post-description">{{ post.description }}</p>
    <!-- Дополнительная информация о посте... -->
    <div class="post-footer">
      <span>Автор: {{ post.author.name }}</span>
      <div class="post-actions">
        <span><i class="fas fa-heart"></i> {{ post.likes }}</span>
        <span><i class="fas fa-comment"></i> {{ post.comments }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.post-detail-container {
  font-family: 'Press Start 2P', cursive;
  background-color: #f5f5f5;
  border: 2px solid #000;
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
  text-align: left;
}

.post-title {
  font-size: 16px;
  margin: 10px 0;
}

.post-description {
  font-size: 14px;
  margin: 10px 0;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  margin-top: 20px;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.post-actions i {
  margin-right: 5px;
}
</style>