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

    async updatePost(postId, name, description) {
        return await performRequest(() => postClient.patch(
            `/${postId}`, 
            { name: name, description: description },
        ));
    }
}

export default new PostService();
