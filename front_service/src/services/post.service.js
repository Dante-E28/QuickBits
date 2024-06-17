import { postClient } from "./axios";
import { performRequest } from "./requestHelper";

class PostService {
    async getPosts() {
        return await performRequest(() => postClient.get(''));
    }

    async createPost(post) {
        return await performRequest(() => postClient.post('', post));
    }

    async getPost(postId) {
        return await performRequest(() => postClient.get(`/${postId}`));
    }
}

export default new PostService();
