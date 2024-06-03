import postClient from "./axios";

class PostService {
    async getPosts() {
        return postClient.get('/posts');
    }

    async createPosts(post) {
        return postClient.post('/posts', post);
    }
}

export default new PostService();
