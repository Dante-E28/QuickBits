import router from "@/router/router";
import { useAuthStore } from "@/stores/auth.store";
import userService from "./user.service";

async function performRequest(request) {
    try {
        const response = await request();
        if (response.status === 200) {
            return response.data;
        } else {
            console.error(`Unexpected status code: ${response.status}`);
            return null;
        }
    } catch(error) {
        if (error.response) {
            console.error('Server error: ', error.response.data);
            console.error('Status code: ', error.response.status);
            console.error('Headers: ', error.response.headers);
            alert(error.response.data.detail.msg);
        } else if (error.request) {
            console.error('Network error: No response received');
            console.error('Request: ', error.request);
        } else {
            console.error('Unexpected error: ', error.message);
        }
        // throw error;
    }
}


async function checkAndRefreshToken() {
    const authStore = useAuthStore();
    const now = new Date().getTime();
    if (authStore.accessExpire <= now) {
        await authStore.refresh();
    }
}

async function patchMeLogoutToLogin(username, email) {
    const authStore = useAuthStore();
    await userService.patchMe({
        'username': username,
        'email': email
    });
    await authStore.logout();
    router.push('/login');
}

export { performRequest, checkAndRefreshToken, patchMeLogoutToLogin };