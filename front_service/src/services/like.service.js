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

    async getLikes(postIds) {
        const params = new URLSearchParams();
        postIds.forEach(id => params.append('post_ids', id));
        
        const response = await performRequest(() => likeClient.get('/likes', { params }));
        return response;
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