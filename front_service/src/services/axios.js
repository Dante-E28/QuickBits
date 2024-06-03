import axios from "axios";
import { useAuthStore } from "@/stores/auth.store";

const INDIE_URL = 'http://localhost:8001';
const AUTH_URL = 'http://localhost:8000';

const postClient = axios.create({
    baseURL: INDIE_URL + '/posts',
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


const authClient = axios.create({
    baseURL: AUTH_URL + '/auth',
    withCredentials: true
});


const userClient = axios.create({
    baseURL: AUTH_URL + '/user',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});

export { postClient, authClient, userClient };