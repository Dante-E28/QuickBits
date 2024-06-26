import { likeClient } from "./axios";
import { performRequest } from "./requestHelper";

class LikeService {
    async createLike(postId, userId) {
        return await performRequest(() => likeClient.post(``, { post_id: postId, user_id: userId }))
    }

    async deleteLike(postId, userId) {
        return await performRequest(() => likeClient.delete(``, {
            data: {
                post_id: postId,
                user_id: userId
            }
        }))
    }

    async getLikesCount(postIds) {
        const params = new URLSearchParams();
        postIds.forEach(id => params.append('post_ids', id));

        console.log('Sending request with params:', params.toString());

        try {
            const response = await performRequest(() => likeClient.get('/likes', { params }));
            console.log('Received response:', response);
            return response;
        } catch (error) {
            console.error('Error while fetching likes:', error);
            throw error;
        }
    }

    async getLike(postId, userId) {
        return await performRequest(() => likeClient.get(`/${postId}`, {
            params: {
                user_id: userId
            }
        }));
    }
}

export default new LikeService();