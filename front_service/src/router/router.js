import { createRouter, createWebHistory } from "vue-router";
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import RegistrationView from '@/views/auth/RegistrationView.vue';
import CreatePostView from '@/views/CreatePostView.vue';
import ProfileView from '@/views/ProfileView.vue';
import ForgottenView from '@/views/auth/ForgottenView.vue';
import EmailVerifyView from '@/views/auth/EmailVerifyView.vue';
import PasswordResetView from "@/views/auth/PasswordResetView.vue";
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
        meta: { requiresAuth: true }
    },
    {
        path: '/profile',
        name: 'ProfileView',
        component: ProfileView,
        meta: { requiresAuth: true }
    },
    {path: '/registration', name: 'RegistrationView', component: RegistrationView},
    {path: '/forgotten', name: 'ForgottenView', component: ForgottenView},
    {
        path: '/email_verification/:token',
        name: 'EmailVerifyView',
        component: EmailVerifyView
    },
    {
        path: '/reset_password/:token',
        name: 'PasswordResetView',
        component: PasswordResetView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
