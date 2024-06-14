VERIFY_EMAIL_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{subject}</title>
    </head>
    <body>
        <p>Здравствуйте,</p>
        <p>Пожалуйста, подтвердите ваш email, перейдя по следующей ссылке:</p>
        <p><a href="{link}">Подтвердить email</a></p>
        <p>Спасибо!</p>
    </body>
    </html>
    """

RESET_PASS_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{subject}</title>
    </head>
    <body>
        <p>Здравствуйте,</p>
        <p>Ссылка для сброса пароля:</p>
        <p><a href="{link}">Сбросить!</a></p>
    </body>
    </html>
    """
