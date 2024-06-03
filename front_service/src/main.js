import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router/router';
import { useAuthStore } from './stores/auth.store';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import './assets/style.css';


const app = createApp(App);
const pinia = createPinia()

app.use(pinia);
app.use(router);

const authStore = useAuthStore();

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        const isAuthChecked = await authStore.checkAuth();
        if (!isAuthChecked) {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

app.mount('#app');
