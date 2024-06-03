<script setup>
import { ref } from 'vue';
import postService from '@/services/post.service';
import { useAuthStore } from '@/stores/auth.store';

const title = ref(null);
const content = ref(null);

const authStore = useAuthStore()


async function submitPost() {
  console.log(authStore.userInfo);
  const post = {
    'name': title.value,
    'description': content.value,
    'user_id': authStore.userInfo.id
  };
  await postService.createPosts(post);
}

</script>

<template>
<div class="create-post-container">
    <h2>Постим?</h2>
    <form>
      <div class="form-group">
        <label for="title">Заголовок</label>
        <input type="text" id="title" v-model="title" required/>
      </div>
      <div class="form-group">
        <label for="content">Содержание</label>
        <textarea id="content" v-model="content" required/>
      </div>
      <button type="submit" @click.prevent="submitPost">Запостить</button>
    </form>
</div>
</template>

<style scoped>
.create-post-container {
  max-width: 500px;
  margin: 30px auto;
  padding: 20px;
  color:#ffffff;
  background-color: #282c34;
  border: 2px solid #286820;
  border-bottom: 3px solid #fc0909;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea {
  width: 400px;
  padding: 8px;
  border: 1px solid #000;
}

textarea {
    width: 400px;
    height: 400px;
}

button {
  padding: 10px 15px;
  border: none;
  cursor: pointer;
}
</style>