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
    
    async deleteComment(commentId) {
        return await performRequest(() => commentClient.delete(`/${commentId}`));
    }

    async updateComment(commentId, text, userId) {
        return await performRequest(() => commentClient.patch(
            `/${commentId}`, 
            { text: text, user_id: userId },
        ));
    }
}

export default new CommentService();