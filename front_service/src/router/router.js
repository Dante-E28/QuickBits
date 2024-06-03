import { createRouter, createWebHistory } from "vue-router";
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import CreatePostView from '@/views/CreatePostView.vue';
import Post from '@/components/Post.vue';
import PostDetail from '@/components/PostDetail.vue';
import TestApi from '@/views/TestApi.vue';


const routes = [
    {path: "/", name: 'HomeView', component: HomeView},
    {path: "/login", name: 'LoginView', component: LoginView},
    {path: "/posts", name: 'Post', component: Post},
    {path: "/post_detail", name: 'PostDetail', component: PostDetail},
    {path: "/test", name: 'Test', component: TestApi},
    {
        path: "/create_post",
        name: 'CreatePostView',
        component: CreatePostView,
        meta: { requiresAuth: true },
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
