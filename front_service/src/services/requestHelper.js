import { apiErrorToConsole, handleApiError } from "./errorHandler";

async function performRequest(request) {
    try {
        const response = await request();
        if (response.status === 200) {
            return response.data;
        } else {
            console.error(`Unexpected status code: ${response.status}`);
            return null;
        }
    } catch(error) {
        apiErrorToConsole(error);
        const message = handleApiError(error);
        throw new Error(message);
    }
}

export { performRequest };