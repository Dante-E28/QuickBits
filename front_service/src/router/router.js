import { createRouter, createWebHistory } from "vue-router";
import Greeting from "@/components/Greeting.vue";
import Login from "@/components/Login.vue";
import Post from '@/components/Post.vue';
import PostDetail from '@/components/PostDetail.vue';
import TestApi from '@/components/TestApi.vue';
import CreatePost from '@/components/CreatePost.vue';


const routes = [
    {path: "/", name: 'Home', component: Greeting},
    {path: "/login", name: 'Login', component: Login},
    {path: "/posts", name: 'Post', component: Post},
    {path: "/post_detail", name: 'PostDetail', component: PostDetail},
    {path: "/test", name: 'Test', component: TestApi},
    {
        path: "/create_post",
        name: 'Create Post',
        component: CreatePost,
        meta: { requiresAuth: true },
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
