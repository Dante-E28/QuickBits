import { defineStore } from "pinia";
import { ref } from "vue";
import AuthService from '../services/auth.service';
import userService from "@/services/user.service";
import router from "@/router/router";

export const useAuthStore = defineStore('auth', () => {
    const userInfo = ref(JSON.parse(localStorage.getItem('userInfo')));
    const accessExpire = ref(localStorage.getItem('accessExpire'));

    const login = async(username, password) => {
        const responseData = await AuthService.login(username, password);
        if (responseData) {
            const userData = await userService.getMe();
            setUserData(userData);
            setTokenData(responseData.expire);
        }
    };

    // const scheduleTokenRefresh = () => {
    //     setTimeout(refresh, accessExpire.value - 60 * 1000);
    // };

    const setTokenData = (expire) => {
        const now = new Date().getTime();
        const expireTime = now + expire * 1000;
        accessExpire.value = expireTime;
        localStorage.setItem('accessExpire', expireTime);
    };

    const setUserData = (userData) => {
        userInfo.value = userData;
        localStorage.setItem('userInfo', JSON.stringify(userData));
    };

    const deleteUserTokenData = () => {
        userInfo.value = null;
        accessExpire.value = null;
        localStorage.removeItem('userInfo');
        localStorage.removeItem('accessExpire');
    };

    const logout = async() => {
        const responseData = await AuthService.logout()
        if (responseData) {
            deleteUserTokenData();
        }
    };

    const refresh = async() => {
        const responseData = await AuthService.refresh();
        if (responseData) {
            setTokenData(responseData.expire);
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

    const patchMeAndLogout = async(username, email) => {
        await userService.patchMe({
            'username': username,
            'email': email
        });
        await logout();
        router.push('/login');
    };

    const register = async(username, email, password) => {
        const responseData = await userService.register({
            'username': username,
            'email': email,
            'password': password
        });
        if (responseData) {
            await login(username, password);
        }
    };

    const verifyEmail = async(token) => {
        const responseData = await AuthService.verifyEmail(token);
        if (responseData) {
            if (userInfo.value) {
                const userData = userInfo.value;
                userData.is_verified = true;
                setUserData(userData);
            }
            return responseData;
        }
    };

    const resetPassword = async(token, password) => {
        const responseData = await AuthService.resetPassword(
            token,
            {'password': password}
        );
        if (responseData) {
            return responseData;
        }
    };

    const sendEmailReset = async(email) => {
        const responseData = await AuthService.sendEmailReset(email);
        if (responseData) {
            return responseData;
        }
    };

    return { 
        userInfo, login, logout, refresh, checkAuth,
        setUserData, patchMeAndLogout, register, verifyEmail,
        resetPassword, sendEmailReset
    };
})