import axios from "axios";
import { useAuthStore } from "@/stores/auth.store";

const POST_URL = 'http://localhost:8001';

const postClient = axios.create({
    baseURL: POST_URL,
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});


postClient.interceptors.request.use(async(config) => {
    const authStore = useAuthStore();
    const now = new Date().getTime();
    if(authStore.accessExpire <= now) {
        await authStore.refresh();
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default postClient;