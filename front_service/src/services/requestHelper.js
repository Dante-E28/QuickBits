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
        if (error.response) {
            console.error('Server error: ', error.response.data);
            console.error('Status code: ', error.response.status);
            console.error('Headers: ', error.response.headers);
        } else if (error.request) {
            console.error('Network error: No response received');
            console.error('Request: ', error.request);
        } else {
            console.error('Unexpected error: ', error.message);
        }
        throw error;
    }
}

export { performRequest };