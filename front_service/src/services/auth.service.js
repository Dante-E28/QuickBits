import axios from "axios";

const AUTH_URL = 'http://localhost:8000/auth/'
const USER_URL = 'http://localhost:8000/user/'

class AuthService {
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        try {
            const response = await axios.post(AUTH_URL + 'login', formData, {
                withCredentials: true
            });
            return {
                'message': response.data.message,
                'accessExpire': response.data.expire
            };
        } catch(error) {
            console.error('Login failed: ', error);
        }
    }

    async fetchUser() {
        try {
            const user = await axios.get(USER_URL + 'me', {
                withCredentials: true
            });
            return user.data;
        } catch(error) {
            console.error('Get user fail: ', error);
            return null;
        }
    }

    async logout() {
        try {
            const response = await axios.post(AUTH_URL + 'logout', {}, {
                withCredentials: true
            });
            return response.data.message; 
        } catch(error) {
            console.error('Loggout failed: ', error);
        }
    }

    async refresh() {
        try {
            const response = await axios.post(AUTH_URL + 'refresh', {}, {
                withCredentials: true
            });
            return {
                'message': response.data.message,
                'accessExpire': response.data.expire
            }
        } catch (error) {
            console.error('Refresh failed: ', error);
        }
    }
}


export default new AuthService()
