import { performRequest } from "./requestHelper";
import { authClient } from "./axios";


class AuthService {
    async login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        return await performRequest(() => authClient.post('/login', formData));
    }

    async logout() {
        return await performRequest(() => authClient.post('/logout'));
    }

    async refresh() {
        return await performRequest(() => authClient.post('/refresh'));
    }

    async verifyEmail(token) {
        return await performRequest(() => authClient.post(`/email_verification/${token}`));
    }

    async resetPassword(token, password) {
        return await performRequest(() => authClient.post(`/reset_password/${token}`, password));
    }

    async sendEmailReset(email) {
        return await performRequest(() => authClient.post(`/reset_password?email=${email}`));
    }
}


export default new AuthService()
