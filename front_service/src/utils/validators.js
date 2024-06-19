function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateUsername(username) {
    const re = /^[A-Za-z0-9]+$/;
    return re.test(username);
}

function validatePassword(password) {
    const re = /^[a-zA-Z\d@$!%*?&]+$/;
    return re.test(password);
}

function validatePasswordDigit(password) {
    const re = /\d/;
    return re.test(password);
}

function validateEmailInput(email) {
    if (!email) {
        return 'Поле почты не заполнено.';
    } else if (!validateEmail(email)) {
        return 'Неправильный формат электронной почты.'
    } else {
        return null;
    }
}

function validateUsernameInput(username) {
    if (!username) {
        return 'Имя пользователя обязательно'
    } else if (username.length < 4) {
        return 'Имя пользователя должно быть не менее 4 символов.'
    } else if (username.length > 16) {
        return 'Имя пользователя должно быть короче 16 символов.'
    } else if (!validateUsername(username)) {
        return 'Юзернейм должен быть из латинских букв и/или цифр.'
    } else {
        return null;
    }
}

function validatePasswordInput(password) {
    if (!password) {
        return 'Пароль обязателен.'
    } else if (password.length < 6) {
        return 'Пароль должен быть 6 и больше символов.'
    } else if (!validatePassword(password)) {
        return 'Используйте в пароле латинские буквы, цифры и спецсимволы.'
    } else if (!validatePasswordDigit(password)) {
        return 'Пароль должен содержать цифры.';
    } else {
        return null;
    }
}
export { validateEmailInput, validateUsernameInput, validatePasswordInput };