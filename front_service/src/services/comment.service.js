import { commentClient } from "./axios";
import { performRequest } from "./requestHelper";

class CommentService {
    async createComment(comment) {
        return await performRequest(() => commentClient.post('', comment));
    }

    async getComments(postId) {
        return await performRequest(() => commentClient.get('', {
            params: {
                post_id: postId
            }
        }));
    }
}

export default new CommentService();