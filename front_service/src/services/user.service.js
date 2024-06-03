import { userClient } from "./axios";
import { performRequest } from "./requestHelper";

class UserService {
    async getMe() {
        return await performRequest(() => userClient.get('/me'));
    }

    async getUser(user_id) {
        return await performRequest(() => userClient.get(`/${user_id}`));
    }
}

export default new UserService();