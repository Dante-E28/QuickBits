import axios from "axios";
import { useAuthStore } from "@/stores/auth.store";

const INDIE_URL = 'http://localhost:8001';
const AUTH_URL = 'http://localhost:8000';

const postEndpointsToCheck = [
    { url: '/posts', methods: ['POST'] }
];

const userEndpointsToCheck = [
    { url: '/me', methods: ['PATCH'] }
];

const postClient = axios.create({
    baseURL: INDIE_URL + '/posts',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});


postClient.interceptors.request.use(async(config) => {
    const shouldCheckToken = postEndpointsToCheck.some(endpoint => 
        config.url.includes(endpoint.url) && endpoint.methods.includes(config.method.toUpperCase())
    );
    
    if (shouldCheckToken) {
        const authStore = useAuthStore();
        await authStore.checkAuth();
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});


const authClient = axios.create({
    baseURL: AUTH_URL + '/auth',
    withCredentials: true
});


const likeClient = axios.create({
    baseURL: INDIE_URL + '/likes',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});


const commentClient = axios.create({
    baseURL: INDIE_URL + '/comments',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});


const userClient = axios.create({
    baseURL: AUTH_URL + '/user',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    }
});


userClient.interceptors.request.use(async(config) => {
    const shouldCheckToken = userEndpointsToCheck.some(endpoint => 
        config.url.includes(endpoint.url) && endpoint.methods.includes(config.method.toUpperCase())
    );
    
    if (shouldCheckToken) {
        const authStore = useAuthStore();
        await authStore.checkAuth();
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export { postClient, authClient, userClient, likeClient, commentClient };