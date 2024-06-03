import { defineStore } from "pinia";
import { ref } from "vue";
import AuthService from '../services/auth.service';

export const useAuthStore = defineStore('auth', () => {
    const userInfo = ref(JSON.parse(localStorage.getItem('userInfo')));
    const accessExpire = ref(localStorage.getItem('accessExpire'));

    const login = async(username, password) => {
        const authData = await AuthService.login(username, password);
        if (authData.message == 'You are logged in!') {
            const userData = await AuthService.fetchUser();
            setUserData(userData);
            setTokenData(authData.accessExpire);
        }
    };

    const scheduleTokenRefresh = (delay) => {
        setTimeout(async () => {
            await refresh()
        }, delay * 1000);
    };

    const setTokenData = (newAccessExpire) => {
        accessExpire.value = new Date().getTime() + newAccessExpire * 1000;
        localStorage.setItem('accessExpire', accessExpire.value);
        scheduleTokenRefresh(newAccessExpire - 60);
    };

    const setUserData = (userData) => {
        userInfo.value = userData;
        localStorage.setItem('userInfo', JSON.stringify(userData));
    };

    const logout = async() => {
        const message = await AuthService.logout()
        if (message == 'You are logged out!') {
            userInfo.value = null;
            accessExpire.value = null;
            localStorage.removeItem('userInfo');
            localStorage.removeItem('accessExpire');
        }
    };

    const refresh = async() => {
        const authData = await AuthService.refresh();
        if (authData.message == 'Token refreshed!') {
            setTokenData(authData.accessExpire);
        } else {
            await logout();
        }
    };

    const checkAuth = async() => {
        if(!userInfo.value) {
            return false;
        }
        const now = new Date().getTime();
        if(accessExpire.value <= now) {
            await refresh();
            return true;
        }
        return true;
    };

    return { userInfo, login, logout, refresh, checkAuth };
})