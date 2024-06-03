<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { computed } from 'vue';

const authStore = useAuthStore()

const currentUser = computed(() => {
    return authStore.userInfo
})
</script>

<template>
  <nav class="navbar">
    <div class="head">
      <div class="d-flex">
        <router-link class="nav-link" to="/test">Лента</router-link>
        <router-link class="navbar-brand mx-5 logo" to="/">QuickBits</router-link>
        <router-link class="nav-link" to="/posts">Инди</router-link>
      </div>
      <div v-if="!currentUser" class="ml-auto">
        <router-link class="nav-link" to="/login">Войти</router-link>
      </div>
      <div v-else class="ml-auto">
        <router-link class="nav-link" to="/profile">{{ currentUser.username }}</router-link>
        <a class="nav-link" @click.prevent="authStore.logout">Выйти</a>
      </div>
    </div>
  </nav>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

.navbar {
  font-family: 'Press Start 2P', cursive;
  padding: 10px 20px;
  background-color: #282c34;
  border-bottom: 2px solid #fc0909;
  flex-wrap: nowrap;
}

.head {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  font-size: 25px;
  position: relative;
}

.navbar-brand, .nav-link {
  color: #ffffff !important;
  font-size: 14px;
}

.navbar-brand {
  font-size: 18px;
  margin: 0;
  padding: 0;
}

.nav-link {
  margin: 0 -2px;
}

.nav-link:hover {
  color: #fc0909 !important;
  transform: scale(1.1);
  /* text-shadow: 0 0 1px #000, 0 0 2px #000; */
}

.logo {
  text-align: center;
}

.d-flex {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav-link {
  flex: 0; /* Убираем flex-grow для уменьшения расстояния */
  text-align: center;
  flex-wrap: nowrap;
}

.ml-auto {
  display: flex;
  align-items: center;
  gap: 1rem; /* Добавляем отступ между элементами пользователя */
  margin-left: auto;
}

a {
  cursor: pointer !important;
}

@media (max-width: 850px) {
  .head {
    flex-direction: row;
    justify-content: space-between;
  }

  .d-flex {
    position: static;
    transform: none;
    flex-direction: row;
    gap: 1rem;
  }

  .navbar-brand {
    margin-right: auto;
  }

  .ml-auto {
    margin-left: 0;
    flex-direction: row;
  }
}
</style>