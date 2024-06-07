function handleApiError(error) {
    let message = 'Произошла ошибка. Попробуйде позже.';
    if (error.response) {
        const checkStruct = error.response.data.detail;
        const msg = checkStruct.msg ? checkStruct.msg : checkStruct[0].msg;
        switch (error.response.status) {
            case 500:
                message = 'Внутренняя ошибка сервера.';
                break;
            default:
                message = msg;
        }
    } else if (error.request) {
        message = 'Нет ответа от сервера. Проверьте интернет-соединение или попробуйте позже.';
    } else {
        message = error.message;
    }
    return message;
}

function apiErrorToConsole(error) {
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
}

export { apiErrorToConsole, handleApiError };