import axios from "axios";

const USER_URL = 'http://localhost:8000/user'


class UserService {
    async getUser(user_id) {
        const formData = new FormData();
        formData.append('user_id', user_id);
        try {
            const response = await axios.get(`${USER_URL}/${user_id}`, {
                withCredentials: true
            });
            return {
                'username': response.data.username // Предполагаем, что ответ содержит username
            };
        } catch (error) {
            console.error(`Failed to fetch user with id ${user_id}`, error);
            return null;
        }
    }
}

export default new UserService();