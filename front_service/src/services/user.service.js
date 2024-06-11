import { userClient } from "./axios";
import { performRequest } from "./requestHelper";

class UserService {
    async getMe() {
        return await performRequest(() => userClient.get('/me'));
    }

    async getUser(user_id) {
        return await performRequest(() => userClient.get(`/${user_id}`));
    }

    async patchMe(user_data) {
        return await performRequest(() => userClient.patch('/me', user_data));
    }

    async register(user_data) {
        return await performRequest(() => userClient.post('', user_data));
    }
}

export default new UserService();