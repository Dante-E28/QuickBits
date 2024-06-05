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
}


export default new AuthService()
